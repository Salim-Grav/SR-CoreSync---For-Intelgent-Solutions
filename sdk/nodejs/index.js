/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

/**
 * S&R CoreSync Official Node.js SDK (@coresync/sdk)
 * Architecture v2.4 LTS - European Cloud & Open Banking Gateway
 */

class CoreSyncError extends Error {
  constructor(message, statusCode = null, responseData = null) {
    super(message);
    this.name = 'CoreSyncError';
    this.statusCode = statusCode;
    this.responseData = responseData;
  }
}

class CoreSyncClient {
  constructor(options = {}) {
    if (typeof options === 'string') {
      this.apiKey = options;
      this.environment = 'production';
    } else {
      this.apiKey = options.apiKey;
      this.environment = options.environment || 'production';
    }

    if (!this.apiKey) {
      throw new Error('CoreSyncClient requires an apiKey to initialize.');
    }

    this.baseUrl = options.baseUrl || 'https://api.sr-coresync.com/v1';
    this.timeout = options.timeout || 30000;
  }

  async _request(method, endpoint, payload = null) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
      'User-Agent': 'CoreSync-Node-SDK/2.4.0',
      'X-CoreSync-Environment': this.environment
    };

    const fetchOptions = {
      method,
      headers
    };

    if (payload && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      fetchOptions.body = JSON.stringify(payload);
    }

    try {
      const response = await fetch(url, fetchOptions);
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new CoreSyncError(`HTTP ${response.status}: ${response.statusText}`, response.status, data);
      }

      return data;
    } catch (err) {
      if (err instanceof CoreSyncError) throw err;
      throw new CoreSyncError(`Network failure communicating with CoreSync API: ${err.message}`);
    }
  }

  /**
   * Generates a BTW & Belastingdienst Compliant Tax Invoice
   */
  async generateInvoice(params) {
    const payload = {
      client_name: params.clientName,
      client_vat: params.clientVat,
      client_email: params.clientEmail,
      amount_net: params.amountNet,
      package_code: params.packageCode || 'SOCIAL_8K_SUITE',
      btw_rate: params.btwRate !== undefined ? params.btwRate : 0.21,
      currency: params.currency || 'EUR'
    };
    return this._request('POST', '/erp/invoices/generate', payload);
  }

  /**
   * Dispatches instant WhatsApp Business API notification
   */
  async triggerWhatsAppNotification(params) {
    const payload = {
      recipient_phone: params.phone,
      invoice_id: params.invoiceId,
      amount: params.amount,
      client_name: params.clientName,
      template: 'financial_settlement_v2026'
    };
    return this._request('POST', '/notifications/whatsapp/dispatch', payload);
  }

  /**
   * Queries double-entry General Ledger records
   */
  async getLedgerEntries(limit = 50) {
    return this._request('GET', `/general-ledger/entries?limit=${limit}`);
  }
}

module.exports = {
  CoreSyncClient,
  CoreSyncError
};
