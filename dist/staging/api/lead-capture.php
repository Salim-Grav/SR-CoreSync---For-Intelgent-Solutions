<?php
/**
 * S&R CoreSync Solutions - Executive Lead Capture & Automation Webhook Gateway
 * Receives consultation booking leads, logs them to a secure local ledger,
 * and relays payloads to external automation webhooks (Make.com, Google Sheets, n8n, Zapier).
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');

// Allow same-origin requests
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$allowedHosts = ['sr-coresync.com', 'www.sr-coresync.com', 'localhost', '127.0.0.1'];
$host = parse_url($origin, PHP_URL_HOST);

if ($origin && in_array($host, $allowedHosts, true)) {
    header("Access-Control-Allow-Origin: $origin");
    header("Access-Control-Allow-Methods: POST, OPTIONS");
    header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");
}

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method not allowed. Use POST.']);
    exit;
}

// Read and decode JSON payload
$rawInput = file_get_contents('php://input');
$data = json_decode($rawInput, true);

if (!$data || !is_array($data)) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Invalid JSON payload.']);
    exit;
}

// Generate unique lead ID if not provided
$leadId = !empty($data['leadId']) ? preg_replace('/[^a-zA-Z0-9_-]/', '', $data['leadId']) : ('LEAD-SR-' . date('Ymd-His') . '-' . substr(bin2hex(random_bytes(4)), 0, 4));

// Sanitize fields
$sanitizedLead = [
    'leadId'         => $leadId,
    'timestamp'      => $data['timestamp'] ?? date('c'),
    'clientName'     => htmlspecialchars(trim($data['clientName'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'companyName'    => htmlspecialchars(trim($data['companyName'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'phone'          => htmlspecialchars(trim($data['phone'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'advisor'        => htmlspecialchars(trim($data['advisor'] ?? 'salim'), ENT_QUOTES, 'UTF-8'),
    'advisorName'    => htmlspecialchars(trim($data['advisorName'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'sessionType'    => htmlspecialchars(trim($data['sessionType'] ?? 'online'), ENT_QUOTES, 'UTF-8'),
    'sessionLabel'   => htmlspecialchars(trim($data['sessionLabel'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'package'        => htmlspecialchars(trim($data['package'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'packageLabel'   => htmlspecialchars(trim($data['packageLabel'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'preferredDate'  => htmlspecialchars(trim($data['preferredDate'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'timeSlot'       => htmlspecialchars(trim($data['timeSlot'] ?? 'afternoon'), ENT_QUOTES, 'UTF-8'),
    'timeSlotLabel'  => htmlspecialchars(trim($data['timeSlotLabel'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'notes'          => htmlspecialchars(trim($data['notes'] ?? ''), ENT_QUOTES, 'UTF-8'),
    'language'       => htmlspecialchars(trim($data['language'] ?? 'ar'), ENT_QUOTES, 'UTF-8'),
    'sourceUrl'      => filter_var($data['sourceUrl'] ?? '', FILTER_SANITIZE_URL),
    'userAgent'      => htmlspecialchars(substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 255), ENT_QUOTES, 'UTF-8'),
    'ipAddress'      => $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0'
];

// 1. Record lead to secure local ledger
$configDir = dirname(__DIR__) . '/config';
$ledgerFile = $configDir . '/leads-ledger.json';

if (!is_dir($configDir)) {
    @mkdir($configDir, 0750, true);
}

$ledgerData = [];
if (file_exists($ledgerFile)) {
    $existing = file_get_contents($ledgerFile);
    $decoded = json_decode($existing, true);
    if (is_array($decoded)) {
        $ledgerData = $decoded;
    }
}

$ledgerData[] = $sanitizedLead;
// Keep the last 1000 leads
if (count($ledgerData) > 1000) {
    $ledgerData = array_slice($ledgerData, -1000);
}

file_put_contents($ledgerFile, json_encode($ledgerData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);

// 2. Relay payload to external Webhook (Make / Google Sheets / n8n / Zapier)
$configFile = $configDir . '/lead-webhook-config.json';
$webhookUrls = [];

if (file_exists($configFile)) {
    $cfg = json_decode(file_get_contents($configFile), true);
    if (!empty($cfg['enabled']) && !empty($cfg['endpoints'])) {
        foreach ($cfg['endpoints'] as $url) {
            if (!empty($url) && filter_var($url, FILTER_VALIDATE_URL)) {
                $webhookUrls[] = $url;
            }
        }
    }
}

$dispatchedTargets = [];

if (!empty($webhookUrls)) {
    foreach ($webhookUrls as $targetUrl) {
        $ch = curl_init($targetUrl);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($sanitizedLead, JSON_UNESCAPED_UNICODE));
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json; charset=utf-8']);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 3); // Fast non-blocking timeout
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
        $res = curl_exec($ch);
        $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        $dispatchedTargets[] = [
            'url'  => parse_url($targetUrl, PHP_URL_HOST),
            'http' => $code
        ];
    }
}

http_response_code(200);
echo json_encode([
    'status'     => 'success',
    'leadId'     => $leadId,
    'recorded'   => true,
    'dispatched' => count($dispatchedTargets),
    'targets'    => $dispatchedTargets,
    'timestamp'  => $sanitizedLead['timestamp']
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
