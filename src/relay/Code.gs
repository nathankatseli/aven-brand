/**
 * AVEN brand book — decisions relay (Google Apps Script web app).
 *
 * Deployed as a Web App (Execute as: Me / Access: Anyone) so the public brand book
 * saves every call to a Google Sheet with NO credentials in the page:
 *   GET                         -> {ok, updated, calls:{id:{label,choice,choiceLabel,note,by,at}}, who:[...]}
 *   POST {calls:{id:{...}}, by} -> upsert those calls (delta), append to Log, return the full state
 *   POST {reset:true, by}       -> clear every call (logged), return the empty state
 *
 * The backing spreadsheet ("AVEN Brand Book — Decisions") is created on first call
 * and its id cached in Script Properties. Every save is also appended to a Log sheet,
 * so nothing is ever lost to an overwrite.
 *
 * Blast radius if someone lifts the URL from the page source: they can write brand-book
 * calls into this one sheet. The Log keeps the history; nothing else is reachable.
 */
var SHEET_NAME = 'Calls';
var LOG_NAME = 'Log';
var HEAD = ['id', 'label', 'choice', 'choiceLabel', 'note', 'by', 'at'];

function getBook_() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('BOOK_ID');
  if (id) {
    try { return SpreadsheetApp.openById(id); } catch (e) { /* recreate below */ }
  }
  var book = SpreadsheetApp.create('AVEN Brand Book — Decisions');
  var s = book.getSheets()[0];
  s.setName(SHEET_NAME);
  s.getRange(1, 1, 1, HEAD.length).setValues([HEAD]);
  book.insertSheet(LOG_NAME).getRange(1, 1, 1, HEAD.length + 1).setValues([HEAD.concat(['action'])]);
  props.setProperty('BOOK_ID', book.getId());
  return book;
}

function state_(book) {
  var s = book.getSheetByName(SHEET_NAME);
  var rows = s.getDataRange().getValues().slice(1);
  var calls = {}, updated = '';
  rows.forEach(function (r) {
    if (!r[0]) return;
    calls[String(r[0])] = { label: String(r[1]), choice: String(r[2]), choiceLabel: String(r[3]), note: String(r[4]), by: String(r[5]), at: String(r[6]) };
    if (String(r[6]) > updated) updated = String(r[6]);
  });
  return { ok: true, book: 'aven-brand', updated: updated, calls: calls };
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return json_(state_(getBook_()));
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    var p = JSON.parse(e.postData.contents);
    if (p.book && p.book !== 'aven-brand') throw new Error('wrong book');
    var by = String(p.by || 'unknown').slice(0, 40);
    var at = new Date().toISOString();
    var book = getBook_();
    var s = book.getSheetByName(SHEET_NAME);
    var log = book.getSheetByName(LOG_NAME);

    if (p.reset === true) {
      var old = s.getDataRange().getValues().slice(1);
      old.forEach(function (r) { if (r[0]) log.appendRow(r.slice(0, 5).concat([by, at, 'reset'])); });
      if (s.getLastRow() > 1) s.deleteRows(2, s.getLastRow() - 1);
      return json_(state_(book));
    }

    var calls = p.calls || {};
    var ids = Object.keys(calls);
    if (!ids.length) throw new Error('no calls');
    var col = s.getRange(1, 1, Math.max(s.getLastRow(), 1), 1).getValues().map(function (r) { return String(r[0]); });
    ids.forEach(function (id) {
      if (!/^[a-z0-9-]{2,40}$/.test(id)) return;
      var c = calls[id] || {};
      var row = [id, String(c.label || '').slice(0, 80), String(c.choice || '').slice(0, 200),
                 String(c.choiceLabel || '').slice(0, 200), String(c.note || '').slice(0, 2000), by, at];
      var idx = col.indexOf(id);
      if (idx > 0) s.getRange(idx + 1, 1, 1, HEAD.length).setValues([row]);
      else { s.appendRow(row); col.push(id); }
      log.appendRow(row.concat([c.choice || c.note ? 'set' : 'clear']));
    });
    return json_(state_(book));
  } catch (err) {
    return json_({ ok: false, error: String(err && err.message || err) });
  } finally {
    try { lock.releaseLock(); } catch (e2) { /* noop */ }
  }
}
