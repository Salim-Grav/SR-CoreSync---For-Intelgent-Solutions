/**
 * =========================================================================
 * S&R CoreSync Solutions - Google Sheets Automated Lead Receiver (Apps Script)
 * =========================================================================
 * 
 * Instructions for Setup in 60 Seconds:
 * 1. Open Google Sheets (create a new sheet or open existing leads spreadsheet).
 * 2. In Google Sheets, click: Extensions (الإضافات) -> Apps Script.
 * 3. Delete any code in the editor, paste this entire file, and click Save.
 * 4. Click: Deploy (نشر) -> New deployment (نشر جديد).
 * 5. Select type: "Web app" (تطبيق ويب).
 * 6. Set Description: "S&R CoreSync Lead Webhook".
 * 7. Set "Execute as": "Me" (حسابك).
 * 8. Set "Who has access": "Anyone" (أي شخص - حتى يتمكن الموقع من إرسال البيانات).
 * 9. Click "Deploy", authorize access, and copy the Web app URL (ينتهي بـ /exec).
 * 10. Paste this URL in your config/lead-webhook-config.json under "googleSheetsWebhookUrl"!
 */

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Ensure header row exists
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "Lead ID",
        "Timestamp (CET)",
        "Client Name",
        "Company Name",
        "Phone / WhatsApp",
        "Advisor",
        "Session Type",
        "Target Package",
        "Preferred Date",
        "Time Slot",
        "Notes / Objectives",
        "Language",
        "Source URL"
      ]);
      // Format headers with royal dark styling
      var headerRange = sheet.getRange(1, 1, 1, 13);
      headerRange.setBackground("#030705");
      headerRange.setFontColor("#d4af37");
      headerRange.setFontWeight("bold");
    }

    var data;
    if (e.postData && e.postData.contents) {
      try {
        data = JSON.parse(e.postData.contents);
      } catch (err) {
        data = e.parameter || {};
      }
    } else {
      data = e.parameter || {};
    }

    var leadId = data.leadId || ("LEAD-SR-" + Utilities.formatDate(new Date(), "CET", "yyyyMMdd-HHmmss"));
    var nowFormatted = Utilities.formatDate(new Date(), "CET", "yyyy-MM-dd HH:mm:ss");

    sheet.appendRow([
      leadId,
      nowFormatted,
      data.clientName || "",
      data.companyName || "",
      data.phone || "",
      data.advisorName || data.advisor || "",
      data.sessionLabel || data.sessionType || "",
      data.packageLabel || data.package || "",
      data.preferredDate || "",
      data.timeSlotLabel || data.timeSlot || "",
      data.notes || "",
      data.language || "",
      data.sourceUrl || ""
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "success", leadId: leadId }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: "online", system: "S&R CoreSync Lead Webhook Gateway" }))
    .setMimeType(ContentService.MimeType.JSON);
}
