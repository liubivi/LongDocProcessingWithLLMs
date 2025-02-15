/** @OnlyCurrentDoc */
/** This is a Google Apps script, applicable to the Spreadsheet created using https://github.com/liubivi/LongDocProcessingWithLLMs/blob/main/README.md */

function formatting() {
  var spreadsheet = SpreadsheetApp.getActive();
  var sheet = spreadsheet.getActiveSheet();

  spreadsheet.setActiveSheet(spreadsheet.getSheetByName('vertimas'), true);
  sheet = spreadsheet.getActiveSheet();
  sheet.getRange(1, 1, sheet.getMaxRows(), sheet.getMaxColumns()).activate();
  spreadsheet.setCurrentCell(spreadsheet.getRange('A2'));
  spreadsheet.getActiveRangeList().setVerticalAlignment('top')
  .setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
  spreadsheet.getActiveSheet().setColumnWidths(1, 26, 418);
  sheet = spreadsheet.getActiveSheet();
  sheet.getRange(1, 1, sheet.getMaxRows(), sheet.getMaxColumns()).activate();
  spreadsheet.getActiveSheet().setColumnWidths(1, 26, 393);
  spreadsheet.setActiveSheet(spreadsheet.getSheetByName('segmentai'), true);
  sheet = spreadsheet.getActiveSheet();
  sheet.getRange(1, 1, sheet.getMaxRows(), sheet.getMaxColumns()).activate();
  spreadsheet.getActiveRangeList().setVerticalAlignment('top')
  .setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
  spreadsheet.getActiveSheet().setColumnWidths(1, 26, 306);
  spreadsheet.getActiveSheet().setFrozenRows(0);
  spreadsheet.getRange('A2').activate();
  spreadsheet.getActiveSheet().setFrozenRows(0);
  spreadsheet.getActiveSheet().setColumnWidth(1, 47);
  spreadsheet.setActiveSheet(spreadsheet.getSheetByName('santrauka'), true);
  spreadsheet.getActiveSheet().setColumnWidth(1, 1067);
  spreadsheet.getRange('A2').activate();
  spreadsheet.getActiveRangeList().setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
  spreadsheet.setActiveSheet(spreadsheet.getSheetByName('segmentai'), true);
  sheet = spreadsheet.getActiveSheet();
  sheet.getRange(1, 1, sheet.getMaxRows(), sheet.getMaxColumns()).activate();
  spreadsheet.getActiveRange().offset(1, 0, spreadsheet.getActiveRange().getNumRows() - 1).sort({column: 1, ascending: true});
};