const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const results = [];
function check(name, condition) {
  results.push({ name, passed: !!condition });
}

// ---------------------------------------------------------------------
// SCR-102 (Job Status Update): dialog open/cancel/save + validation
// ---------------------------------------------------------------------
const scr102Path = path.join(__dirname, 'SCR-102', 'mockup.html');
const scr102Html = fs.readFileSync(scr102Path, 'utf8');
const dom102 = new JSDOM(scr102Html, { runScripts: 'dangerously', resources: 'usable' });
const doc102 = dom102.window.document;

// Initial state: Update Status button must be disabled (no status chosen yet)
const updateBtn = doc102.getElementById('update-status-btn');
check('SCR-102: Update Status button starts disabled', updateBtn.disabled === true);

// Select a status -> button should become enabled
const statusSelect = doc102.getElementById('new-status-select');
statusSelect.value = 'On-Site';
statusSelect.dispatchEvent(new dom102.window.Event('change'));
check('SCR-102: Update Status button enabled after selecting a status', updateBtn.disabled === false);

// Dialog starts hidden
const dialog = doc102.getElementById('confirm-dialog');
check('SCR-102: confirm dialog starts hidden', dialog.hidden === true);

// Click Update Status -> dialog opens, value populated
updateBtn.dispatchEvent(new dom102.window.Event('click'));
check('SCR-102: dialog opens on Update Status click', dialog.hidden === false);
check('SCR-102: dialog shows the chosen status value', doc102.getElementById('confirm-dialog-value').textContent === 'On-Site');

// Click Cancel -> dialog closes, current status UNCHANGED
const currentStatusEl = doc102.getElementById('current-status');
const statusBeforeCancel = currentStatusEl.textContent;
doc102.getElementById('confirm-cancel-btn').dispatchEvent(new dom102.window.Event('click'));
check('SCR-102: dialog closes on Cancel', dialog.hidden === true);
check('SCR-102: Cancel does NOT apply the status change', currentStatusEl.textContent === statusBeforeCancel && statusBeforeCancel === 'En Route');

// Re-open and this time Confirm -> dialog closes, status DOES change
updateBtn.dispatchEvent(new dom102.window.Event('click'));
check('SCR-102: dialog re-opens for second attempt', dialog.hidden === false);
doc102.getElementById('confirm-save-btn').dispatchEvent(new dom102.window.Event('click'));
check('SCR-102: dialog closes on Confirm (save)', dialog.hidden === true);
check('SCR-102: Confirm DOES apply the status change', currentStatusEl.textContent === 'On-Site');

// ---------------------------------------------------------------------
// SCR-101 (Dispatch Queue): assign validation + inline confirmation
// ---------------------------------------------------------------------
const scr101Path = path.join(__dirname, 'SCR-101', 'mockup.html');
const scr101Html = fs.readFileSync(scr101Path, 'utf8');
const dom101 = new JSDOM(scr101Html, { runScripts: 'dangerously', resources: 'usable' });
const doc101 = dom101.window.document;

const assignBtn = doc101.getElementById('assign-btn');
check('SCR-101: Assign button starts disabled', assignBtn.disabled === true);

const techSelect = doc101.getElementById('technician-select');
const timeInput = doc101.getElementById('time-slot-input');

// Only technician chosen, no time slot -> still disabled
techSelect.value = 'J. Alvarez';
techSelect.dispatchEvent(new dom101.window.Event('change'));
check('SCR-101: Assign button still disabled with only technician chosen', assignBtn.disabled === true);

// Now add a time slot -> enabled
timeInput.value = 'Tomorrow 9am-12pm';
timeInput.dispatchEvent(new dom101.window.Event('input'));
check('SCR-101: Assign button enabled once both technician and time slot are set', assignBtn.disabled === false);

// Click Assign -> assigned cell updates, confirmation shown
const assignedCell = doc101.getElementById('assigned-technician-cell');
assignBtn.dispatchEvent(new dom101.window.Event('click'));
check('SCR-101: assigned technician cell updates on Assign', assignedCell.textContent.includes('J. Alvarez'));
check('SCR-101: confirmation message shown after Assign', doc101.getElementById('assign-confirmation').style.display === 'inline');

// ---------------------------------------------------------------------
// Report
// ---------------------------------------------------------------------
console.log('');
let allPassed = true;
for (const r of results) {
  console.log((r.passed ? 'PASS' : 'FAIL') + ': ' + r.name);
  if (!r.passed) allPassed = false;
}
console.log('');
console.log(allPassed ? `ALL ${results.length} CHECKS PASSED` : 'SOME CHECKS FAILED');
process.exit(allPassed ? 0 : 1);
