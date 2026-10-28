/**
 * GSOリフォーム 契約書LINEボット
 *
 * LINEグループに投稿された請負契約書の写真を受け取り、
 * Claudeで項目を読み取り、「【GSOリフォーム】経営管理帳票」の
 * 「入金管理」シートに1行追記し、読み取り結果をグループに返信する。
 *
 * 書き込む列（入力列のみ）: B契約日 C代理店 D担当者 E顧客名 Fカテゴリ G契約金額 M入金予定日 O入金状況 Q支払通知書 S備考
 * 触らない列（数式）  : A契約月 H標準料率 J適用料率 K受領額 L払出額
 *
 * スクリプトプロパティ（プロジェクトの設定 > スクリプト プロパティ）:
 *   LINE_CHANNEL_ACCESS_TOKEN  LINE Messaging API の長期チャネルアクセストークン
 *   ANTHROPIC_API_KEY          Anthropic APIキー
 *   SPREADSHEET_ID             1q9cTqWUhwjcBfwF5-hufukyoQkGJC8kcH0_awnQA8FE
 *   DRIVE_FOLDER_ID            契約書写真の保存先フォルダID
 *   ALLOWED_GROUP_IDS          （任意）反応するグループIDをカンマ区切り。空なら全グループ
 */

const CONFIG = {
  SHEET_LEDGER: '入金管理',
  SHEET_MASTER: 'マスタ',
  SHEET_STAFF: 'LINE連携',
  SHEET_LOG: 'LINE処理ログ',
  LEDGER_FIRST_DATA_ROW: 5,
  CLAUDE_MODEL: 'claude-opus-5-5',
  CLAUDE_EFFORT: 'high',
  DEFAULT_PAYMENT_STATUS: '未入金',
  DEFAULT_NOTICE_STATUS: '未作成',
};

const COL = { DATE: 2, AGENCY: 3, STAFF: 4, CUSTOMER: 5, CATEGORY: 6, AMOUNT: 7, DUE: 13, PAID_ON: 14, STATUS: 15, NOTICE: 17, NOTE: 19 };
const FORMULA_COLS = [1, 8, 10, 11, 12]; // A, H, J, K, L

function prop_(key, optional) {
  const v = PropertiesService.getScriptProperties().getProperty(key);
  if (!v && !optional) throw new Error('スクリプトプロパティ ' + key + ' が未設定です');
  return v || '';
}

// ---------------------------------------------------------------------------
// 初期セットアップ（エディタから1回だけ実行）
// ---------------------------------------------------------------------------
function setup() {
  const ss = SpreadsheetApp.openById(prop_('SPREADSHEET_ID'));
  let staff = ss.getSheetByName(CONFIG.SHEET_STAFF);
  if (!staff) {
    staff = ss.insertSheet(CONFIG.SHEET_STAFF);
    staff.getRange(1, 1, 1, 4).setValues([['担当者', '代理店', 'LINE表示名', 'LINE userId']]);
    staff.getRange(2, 1, 3, 4).setValues([
      ['宮下', 'エナジージャパン', '', ''],
      ['治部', 'GSOライフケア', '', ''],
      ['伊藤', 'GSOライフケア', '', ''],
    ]);
    staff.setFrozenRows(1);
  }
  let log = ss.getSheetByName(CONFIG.SHEET_LOG);
  if (!log) {
    log = ss.insertSheet(CONFIG.SHEET_LOG);
    log.getRange(1, 1, 1, 7).setValues([['処理日時', 'LINE messageId', '投稿者', '結果', '台帳行', '要確認', '画像リンク']]);
    log.setFrozenRows(1);
  }
  Logger.log('セットアップ完了。ウェブアプリとしてデプロイし、URLをLINE DevelopersのWebhook URLに設定してください。');
}

// ---------------------------------------------------------------------------
// LINE Webhook 入口
// ---------------------------------------------------------------------------
function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    (body.events || []).forEach(handleEvent_);
  } catch (err) {
    console.error('doPost error: ' + err + '\n' + err.stack);
  }
  return ContentService.createTextOutput('ok');
}

function handleEvent_(ev) {
  if (ev.type !== 'message' || !ev.message || ev.message.type !== 'image') return;
  const allowed = prop_('ALLOWED_GROUP_IDS', true).split(',').map(s => s.trim()).filter(Boolean);
  const chatId = ev.source.groupId || ev.source.roomId || ev.source.userId;
  if (allowed.length && allowed.indexOf(chatId) < 0) return;
  if (alreadyProcessed_(ev.message.id)) return; // LINEの再送対策

  const imageSet = ev.message.imageSet; // 複数枚同時送信のとき付く {id, index, total}
  let messageIds = [ev.message.id];
  if (imageSet && imageSet.total > 1) {
    const cache = CacheService.getScriptCache();
    const key = 'imgset_' + imageSet.id;
    const got = JSON.parse(cache.get(key) || '[]');
    got.push(ev.message.id);
    cache.put(key, JSON.stringify(got), 21600);
    if (got.length < imageSet.total) return; // 全部揃うまで待つ
    messageIds = got;
    cache.remove(key);
  }

  const sender = senderName_(ev.source);
  processContractImages_(messageIds, sender, ev.replyToken, chatId);
}

// ---------------------------------------------------------------------------
// 本体: 画像取得 → Claude抽出 → 台帳追記 → 返信
// ---------------------------------------------------------------------------
function processContractImages_(messageIds, sender, replyToken, chatId) {
  const images = messageIds.map(id => ({ id: id, blob: fetchLineContent_(id) }));
  const ss = SpreadsheetApp.openById(prop_('SPREADSHEET_ID'));
  const categories = readCategories_(ss);
  const staffMap = readStaffMap_(ss);

  let result;
  try {
    result = extractWithClaude_(images.map(i => i.blob), categories);
  } catch (err) {
    logRow_(ss, messageIds.join(','), sender, '読み取り失敗: ' + err, '', '', '');
    reply_(replyToken, chatId, '⚠ 契約書の読み取りに失敗しました。\n' + String(err).slice(0, 200) + '\n手入力をお願いします。');
    return;
  }

  const contracts = (result.contracts || []).filter(c => c.is_contract_front_page);
  if (!contracts.length) {
    logRow_(ss, messageIds.join(','), sender, '契約書の表面ではない', '', '', '');
    return; // 約款ページ・見積書などは黙って無視
  }

  const replies = [];
  contracts.forEach(c => {
    const row = buildLedgerRow_(c, sender, staffMap, categories);
    const fileUrl = saveImages_(images, row);
    row.note = [row.note, '契約書: ' + fileUrl].filter(Boolean).join(' / ');

    const ledger = ss.getSheetByName(CONFIG.SHEET_LEDGER);
    const dup = findDuplicate_(ledger, row);
    if (dup) {
      logRow_(ss, messageIds.join(','), sender, '登録済み', dup.rowNumber, row.flags.join(' / '), fileUrl);
      replies.push(duplicateMessage_(row, dup));
      return;
    }
    const n = appendLedgerRow_(ledger, row);
    logRow_(ss, messageIds.join(','), sender, '追記', n, row.flags.join(' / '), fileUrl);
    replies.push(successMessage_(row, n));
  });
  reply_(replyToken, chatId, replies.join('\n\n'));
}

// ---------------------------------------------------------------------------
// Claude 読み取り
// ---------------------------------------------------------------------------
function extractionSchema_(categories) {
  const money = { anyOf: [{ type: 'integer' }, { type: 'null' }] };
  const str = { anyOf: [{ type: 'string' }, { type: 'null' }] };
  return {
    type: 'object',
    additionalProperties: false,
    required: ['contracts'],
    properties: {
      contracts: {
        type: 'array',
        items: {
          type: 'object',
          additionalProperties: false,
          required: ['is_contract_front_page', 'work_title', 'work_address', 'contract_date', 'work_start', 'work_end',
            'amount_tax_included', 'amount_tax_excluded', 'tax_amount', 'payments', 'customer_family_name',
            'customer_given_name', 'customer_phone', 'customer_address', 'staff_name', 'category', 'category_confidence',
            'unreadable_fields', 'notes'],
          properties: {
            is_contract_front_page: { type: 'boolean' },
            work_title: str,
            work_address: str,
            contract_date: { anyOf: [{ type: 'string' }, { type: 'null' }], description: 'YYYY-MM-DD。下部の「日付」欄。空欄なら支払方法の契約締結時の日付' },
            work_start: str,
            work_end: str,
            amount_tax_included: money,
            amount_tax_excluded: money,
            tax_amount: money,
            payments: {
              type: 'array',
              items: {
                type: 'object',
                additionalProperties: false,
                required: ['timing', 'date', 'amount'],
                properties: {
                  timing: { type: 'string', enum: ['契約締結時', '着工時', '完工時', 'その他'] },
                  date: str,
                  amount: money,
                },
              },
            },
            customer_family_name: str,
            customer_given_name: str,
            customer_phone: str,
            customer_address: str,
            staff_name: str,
            category: { type: 'string', enum: categories },
            category_confidence: { type: 'string', enum: ['high', 'low'] },
            unreadable_fields: { type: 'array', items: { type: 'string' } },
            notes: str,
          },
        },
      },
    },
  };
}

function extractionPrompt_(categories) {
  return [
    'あなたはGSOリフォーム株式会社の経理アシスタントです。LINEで送られてきた「住宅リフォーム工事 請負契約書」の写真を読み取り、台帳に入力する項目をJSONで返してください。',
    '',
    '## 書式（毎回同じ用紙）',
    '1. 工事名称 / 2. 工事場所 / 3. 工事期間（年月日より年月日まで）',
    '4. 請負金額: 請負金額（税込）・うち工事価格（税抜）・消費税等額',
    '5. 支払方法: 契約締結時・着工時・完工時・（予備行）それぞれに 年月日 と 金額（税込）',
    '6. 添付書類 / 日付（契約日） / 注文者（住所・氏名・電話番号、2人分の欄がある）/ 請負者（GSOリフォーム株式会社、担当者欄に手書きのサイン）',
    '',
    '## ルール',
    '- 年号は和暦です。「令和8年」「R8年」「令8年」はすべて 2026年。令和N年 = 2018+N 年。日付は YYYY-MM-DD で返す。',
    '- 金額は手書きの「¥4,983,000-」「826.925」のような表記。区切りのカンマやピリオドは桁区切りなので、整数円で返す（826.925 → 826925）。',
    '- 金額欄の「×」「0」「ー」は 0 円。空欄は null。',
    '- 請負金額（税込）は必ず「うち工事価格 + 消費税等額」と一致するはず。一致しない場合は税込欄の数字を優先し、notes に矛盾を書く。',
    '- 契約日は下部の「日付」欄。空欄なら支払方法の「契約締結時」の年月日。それも無ければ null。',
    '- 注文者の氏名は姓と名を分けて返す。注文者欄が2人分埋まっている場合は左側（1人目）を customer にし、2人目は notes に書く。',
    '- 担当者は請負者欄の「担当者:」の右にある手書きサイン（例: 宮下、伊藤、治部）。印影の文字も手がかりにしてよい。読めなければ null。',
    '- 読めない・自信がない項目は unreadable_fields に項目名を入れる。推測で埋めない。',
    '- category は工事名称から次の一覧の中で最も近いものを選ぶ: ' + categories.join(' / '),
    '  目安: 床下・基礎・防蟻・防腐・調湿 → 床下工事 / 屋根・外壁・塗装・漆喰・棟・屋根裏 → 屋根・外壁 / 給湯器 → ガス給湯器 または エコキュート / 判断に迷う → その他リフォーム にして category_confidence を low。',
    '- 請負契約書の表面（上記の書式）以外の写真（約款ページ・見積書・別の書類）は is_contract_front_page を false にする。',
    '- 複数枚の写真に同じ契約書が写っている場合は1件にまとめる。別の契約が複数写っている場合はそれぞれ1件ずつ返す。',
  ].join('\n');
}

function extractWithClaude_(blobs, categories) {
  const content = blobs.map(b => ({
    type: 'image',
    source: { type: 'base64', media_type: b.getContentType() || 'image/jpeg', data: Utilities.base64Encode(b.getBytes()) },
  }));
  content.push({ type: 'text', text: '上記の写真から契約書の項目を読み取ってください。' });

  const payload = {
    model: CONFIG.CLAUDE_MODEL,
    max_tokens: 16000,
    system: extractionPrompt_(categories),
    messages: [{ role: 'user', content: content }],
    output_config: { effort: CONFIG.CLAUDE_EFFORT, format: { type: 'json_schema', schema: extractionSchema_(categories) } },
    fallbacks: 'default',
  };
  const res = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': prop_('ANTHROPIC_API_KEY'),
      'anthropic-version': '2026-10-21',
      'anthropic-beta': 'server-side-fallback-2026-07-01',
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true,
  });
  if (res.getResponseCode() !== 200) throw new Error('Claude API ' + res.getResponseCode() + ': ' + res.getContentText().slice(0, 300));
  const msg = JSON.parse(res.getContentText());
  if (msg.stop_reason === 'refusal') throw new Error('Claudeが処理を拒否しました');
  const text = (msg.content || []).filter(b => b.type === 'text').map(b => b.text).join('');
  return JSON.parse(text);
}

// ---------------------------------------------------------------------------
// 台帳行の組み立て
// ---------------------------------------------------------------------------
function buildLedgerRow_(c, sender, staffMap, categories) {
  const flags = (c.unreadable_fields || []).slice();

  // 担当者 → 代理店。契約書の担当者サインを優先し、無ければLINE投稿者で推定
  let staff = normalizeStaff_(c.staff_name, staffMap);
  let agency = staff ? staffMap[staff] : '';
  if (!staff) {
    const bySender = staffBySender_(sender, staffMap);
    if (bySender) { staff = bySender; agency = staffMap[staff]; flags.push('担当者欄が空欄のためLINE投稿者(' + sender + ')から推定'); }
    else flags.push('担当者・代理店が特定できず（空欄）');
  }

  const customer = normalizeName_(c.customer_family_name, c.customer_given_name);
  if (!customer) flags.push('顧客名');

  const amount = c.amount_tax_included;
  if (amount == null) flags.push('契約金額');
  else if (c.amount_tax_excluded != null && c.tax_amount != null && c.amount_tax_excluded + c.tax_amount !== amount) {
    flags.push('税込金額と内訳が不一致(' + c.amount_tax_excluded + '+' + c.tax_amount + ')');
  }

  const contractDate = parseDate_(c.contract_date);
  if (!contractDate) flags.push('契約日');

  const due = pickDueDate_(c.payments || [], amount);
  if (!due) flags.push('入金予定日（支払方法欄に完工時の日付なし）');

  let category = categories.indexOf(c.category) >= 0 ? c.category : '未分類';
  if (c.category_confidence !== 'high' || category === '未分類') flags.push('カテゴリ');

  const noteParts = [];
  if (c.work_title) noteParts.push('工事: ' + c.work_title);
  if (c.work_address) noteParts.push('場所: ' + c.work_address);
  if (c.customer_phone) noteParts.push('TEL: ' + c.customer_phone);
  if (c.work_start || c.work_end) noteParts.push('工期: ' + (c.work_start || '?') + '〜' + (c.work_end || '?'));
  if (c.notes) noteParts.push(c.notes);
  noteParts.push('LINE自動登録(' + sender + ')');
  if (flags.length) noteParts.push('要確認: ' + flags.join('、'));

  return {
    contractDate: contractDate, agency: agency, staff: staff, customer: customer, category: category,
    amount: amount, due: due, note: noteParts.join(' / '), flags: flags, workTitle: c.work_title || '',
  };
}

// LINE表示名（例: 「宮下 幸雄」「GSO 伊藤」）から担当者を推定
function staffBySender_(sender, staffMap) {
  if (!sender) return '';
  const n = String(sender).replace(/[\s　]/g, '');
  const keys = Object.keys(staffMap.__bySender);
  for (const k of keys) if (k && n.indexOf(k.replace(/[\s　]/g, '')) >= 0) return staffMap.__bySender[k];
  return '';
}

function normalizeStaff_(name, staffMap) {
  if (!name) return '';
  const n = String(name).replace(/[\s　]/g, '');
  const keys = Object.keys(staffMap).filter(k => k !== '__bySender');
  for (const k of keys) if (n.indexOf(k) >= 0 || k.indexOf(n) >= 0) return k;
  return '';
}

function normalizeName_(family, given) {
  const f = (family || '').replace(/[\s　]/g, '');
  const g = (given || '').replace(/[\s　]/g, '');
  if (!f && !g) return '';
  return g ? f + '　' + g : f; // 姓と名の間は全角スペースで統一
}

function parseDate_(s) {
  if (!s) return null;
  const m = String(s).match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
  if (!m) return null;
  const d = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  return isNaN(d.getTime()) ? null : d;
}

// 入金予定日 = 完工時の日付（金額が入っていれば）。無ければ金額>0の最後の支払予定日。
function pickDueDate_(payments, total) {
  const paid = payments.filter(p => p.amount != null && p.amount > 0 && parseDate_(p.date));
  if (!paid.length) return null;
  const completion = paid.filter(p => p.timing === '完工時');
  const pick = completion.length ? completion[0] : paid[paid.length - 1];
  return parseDate_(pick.date);
}

function readCategories_(ss) {
  const vals = ss.getSheetByName(CONFIG.SHEET_MASTER).getRange('L5:L30').getValues().map(r => String(r[0]).trim()).filter(Boolean);
  return vals.length ? vals : ['未分類'];
}

function readStaffMap_(ss) {
  const sh = ss.getSheetByName(CONFIG.SHEET_STAFF);
  const map = { __bySender: {} };
  if (!sh) return map;
  sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 4).getValues().forEach(r => {
    const staff = String(r[0]).trim(), agency = String(r[1]).trim(), display = String(r[2]).trim();
    if (!staff) return;
    map[staff] = agency;
    if (display) map.__bySender[display] = staff;
    map.__bySender[staff] = staff; // 表示名が担当者名そのものの場合
  });
  return map;
}

// ---------------------------------------------------------------------------
// 台帳の読み書き
// ---------------------------------------------------------------------------
function ledgerRows_(ledger) {
  const last = ledger.getLastRow();
  if (last < CONFIG.LEDGER_FIRST_DATA_ROW) return [];
  const vals = ledger.getRange(CONFIG.LEDGER_FIRST_DATA_ROW, 1, last - CONFIG.LEDGER_FIRST_DATA_ROW + 1, COL.NOTE).getValues();
  return vals.map((r, i) => ({
    rowNumber: CONFIG.LEDGER_FIRST_DATA_ROW + i,
    date: r[COL.DATE - 1], agency: r[COL.AGENCY - 1], staff: r[COL.STAFF - 1], customer: String(r[COL.CUSTOMER - 1] || ''),
    amount: Number(r[COL.AMOUNT - 1]) || 0,
  }));
}

function isDate_(d) { return !!d && typeof d.getTime === 'function' && !isNaN(d.getTime()); }

function sameDay_(a, b) {
  return isDate_(a) && isDate_(b) && a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}

function findDuplicate_(ledger, row) {
  if (row.amount == null) return null;
  const key = row.customer.replace(/[\s　]/g, '');
  const rows = ledgerRows_(ledger).filter(r => isDate_(r.date));
  for (const r of rows) {
    if (r.amount !== row.amount) continue;
    const rKey = r.customer.replace(/[\s　]/g, '');
    const sameCustomer = key && rKey && (key === rKey || key.indexOf(rKey) === 0 || rKey.indexOf(key) === 0);
    if (sameCustomer || (row.contractDate && sameDay_(r.date, row.contractDate))) return r;
  }
  return null;
}

function appendLedgerRow_(ledger, row) {
  const rows = ledgerRows_(ledger);
  let n = CONFIG.LEDGER_FIRST_DATA_ROW;
  rows.forEach(r => { if (r.date !== '' && r.date != null) n = r.rowNumber + 1; });
  if (n > ledger.getMaxRows()) ledger.insertRowsAfter(ledger.getMaxRows(), 10);

  // 数式列が空なら1つ上の行からコピー（書式も引き継ぐ）
  const prev = n - 1;
  FORMULA_COLS.forEach(col => {
    const cell = ledger.getRange(n, col);
    if (!cell.getFormula() && prev >= CONFIG.LEDGER_FIRST_DATA_ROW) {
      ledger.getRange(prev, col).copyTo(cell, SpreadsheetApp.CopyPasteType.PASTE_FORMULA, false);
    }
  });

  const set = (col, v) => ledger.getRange(n, col).setValue(v);
  set(COL.DATE, row.contractDate || '');
  set(COL.AGENCY, row.agency || '');
  set(COL.STAFF, row.staff || '');
  set(COL.CUSTOMER, row.customer || '');
  set(COL.CATEGORY, row.category || '未分類');
  set(COL.AMOUNT, row.amount == null ? '' : row.amount);
  set(COL.DUE, row.due || '');
  set(COL.STATUS, CONFIG.DEFAULT_PAYMENT_STATUS);
  set(COL.NOTICE, CONFIG.DEFAULT_NOTICE_STATUS);
  set(COL.NOTE, row.note || '');
  return n;
}

function logRow_(ss, messageId, sender, result, rowNumber, flags, fileUrl) {
  const sh = ss.getSheetByName(CONFIG.SHEET_LOG);
  if (sh) sh.appendRow([new Date(), messageId, sender, result, rowNumber, flags, fileUrl]);
}

function alreadyProcessed_(messageId) {
  const ss = SpreadsheetApp.openById(prop_('SPREADSHEET_ID'));
  const sh = ss.getSheetByName(CONFIG.SHEET_LOG);
  if (!sh || sh.getLastRow() < 2) return false;
  const ids = sh.getRange(2, 2, sh.getLastRow() - 1, 1).getValues().map(r => String(r[0]));
  return ids.some(v => v.split(',').indexOf(String(messageId)) >= 0);
}

// ---------------------------------------------------------------------------
// LINE API
// ---------------------------------------------------------------------------
function lineHeaders_() {
  return { Authorization: 'Bearer ' + prop_('LINE_CHANNEL_ACCESS_TOKEN') };
}

function fetchLineContent_(messageId) {
  const res = UrlFetchApp.fetch('https://api-data.line.me/v2/bot/message/' + messageId + '/content', { headers: lineHeaders_(), muteHttpExceptions: true });
  if (res.getResponseCode() !== 200) throw new Error('LINE画像取得失敗 ' + res.getResponseCode());
  return res.getBlob().setName(messageId + '.jpg');
}

function senderName_(source) {
  try {
    let url;
    if (source.groupId) url = 'https://api.line.me/v2/bot/group/' + source.groupId + '/member/' + source.userId;
    else if (source.roomId) url = 'https://api.line.me/v2/bot/room/' + source.roomId + '/member/' + source.userId;
    else url = 'https://api.line.me/v2/bot/profile/' + source.userId;
    const res = UrlFetchApp.fetch(url, { headers: lineHeaders_(), muteHttpExceptions: true });
    if (res.getResponseCode() === 200) return JSON.parse(res.getContentText()).displayName || '';
  } catch (e) { /* 表示名が取れなくても処理は続ける */ }
  return '';
}

function reply_(replyToken, chatId, text) {
  const headers = Object.assign({ 'Content-Type': 'application/json' }, lineHeaders_());
  const messages = [{ type: 'text', text: text.slice(0, 4900) }];
  let ok = false;
  if (replyToken) {
    const r = UrlFetchApp.fetch('https://api.line.me/v2/bot/message/reply', { method: 'post', headers: headers, payload: JSON.stringify({ replyToken: replyToken, messages: messages }), muteHttpExceptions: true });
    ok = r.getResponseCode() === 200;
  }
  if (!ok && chatId) { // replyTokenの期限切れ時はpushで送る（無料枠の通数を消費）
    UrlFetchApp.fetch('https://api.line.me/v2/bot/message/push', { method: 'post', headers: headers, payload: JSON.stringify({ to: chatId, messages: messages }), muteHttpExceptions: true });
  }
}

// ---------------------------------------------------------------------------
// Drive 保存・返信文
// ---------------------------------------------------------------------------
function saveImages_(images, row) {
  const folder = DriveApp.getFolderById(prop_('DRIVE_FOLDER_ID'));
  const d = row.contractDate || new Date();
  const stamp = Utilities.formatDate(d, 'Asia/Tokyo', 'yyyyMMdd');
  let firstUrl = '';
  images.forEach((img, i) => {
    const name = stamp + '_' + (row.customer || '不明').replace(/[\s　]/g, '') + '_契約書' + (images.length > 1 ? '_' + (i + 1) : '') + '.jpg';
    const f = folder.createFile(img.blob.copyBlob().setName(name));
    if (!firstUrl) firstUrl = f.getUrl();
  });
  return firstUrl;
}

function yen_(n) { return n == null ? '不明' : '¥' + Number(n).toLocaleString('ja-JP'); }
function ymd_(d) { return d ? Utilities.formatDate(d, 'Asia/Tokyo', 'yyyy/MM/dd') : '不明'; }

function successMessage_(row, n) {
  const lines = [
    '📄 契約書を台帳に登録しました（入金管理 ' + n + '行目）',
    '顧客名：' + (row.customer || '不明'),
    '工事：' + (row.workTitle || '不明'),
    '代理店／担当：' + (row.agency || '未設定') + '／' + (row.staff || '未設定'),
    '契約日：' + ymd_(row.contractDate),
    '契約金額（税込）：' + yen_(row.amount),
    '入金予定日：' + ymd_(row.due),
    'カテゴリ：' + row.category,
  ];
  if (row.flags.length) lines.push('⚠ 要確認：' + row.flags.join('、'));
  lines.push('違っていたらシートの' + n + '行目を直接修正してください。');
  return lines.join('\n');
}

function duplicateMessage_(row, dup) {
  const lines = [
    '⚠ この契約書は登録済みと判断しました（入金管理 ' + dup.rowNumber + '行目）',
    '台帳：' + dup.customer + ' / ' + yen_(dup.amount) + ' / ' + ymd_(dup.date) + ' / ' + dup.agency + '／' + dup.staff,
    '読取：' + (row.customer || '不明') + ' / ' + yen_(row.amount) + ' / ' + ymd_(row.contractDate) + ' / ' + (row.agency || '?') + '／' + (row.staff || '?'),
  ];
  if (dup.customer.replace(/[\s　]/g, '') !== row.customer.replace(/[\s　]/g, '')) lines.push('❗顧客名が台帳と違います。' + dup.rowNumber + '行目を確認してください。');
  lines.push('別の契約なら、金額か顧客名を変えて再投稿せず、シートに直接追記してください。');
  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// 手動テスト（エディタから実行。Driveに置いた写真で動作確認する）
// ---------------------------------------------------------------------------
function testWithDriveFile() {
  const fileId = 'ここにDriveの画像ファイルIDを入れる';
  const blob = DriveApp.getFileById(fileId).getBlob();
  const ss = SpreadsheetApp.openById(prop_('SPREADSHEET_ID'));
  const result = extractWithClaude_([blob], readCategories_(ss));
  Logger.log(JSON.stringify(result, null, 2));
  const row = buildLedgerRow_(result.contracts[0], 'テスト', readStaffMap_(ss), readCategories_(ss));
  Logger.log(JSON.stringify(row, null, 2));
  const dup = findDuplicate_(ss.getSheetByName(CONFIG.SHEET_LEDGER), row);
  Logger.log(dup ? '登録済み: ' + dup.rowNumber + '行目' : '未登録（本番なら追記される）');
}
