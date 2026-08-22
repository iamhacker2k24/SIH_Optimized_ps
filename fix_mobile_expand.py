from bs4 import BeautifulSoup
import re
import html

html_path = r'c:\Users\mrdeb\Desktop\html\index.html.bak'
output_path = r'c:\Users\mrdeb\Desktop\html\index.html'

print("Reading index.html.bak...")
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

tbody = soup.find('tbody')
rows = tbody.find_all('tr', recursive=False)

print(f"Extracting data from {len(rows)} rows...")

ps_data_list = []

for idx, r in enumerate(rows):
    tds = r.find_all('td', recursive=False)
    if len(tds) < 8:
        continue
    
    sno = tds[0].get_text(strip=True)
    org = tds[1].get_text(strip=True)
    category = tds[3].get_text(strip=True)
    ps_number = tds[4].get_text(strip=True)
    theme = tds[6].get_text(strip=True)
    
    title_td = tds[2]
    title_a = title_td.find('a')
    title = title_a.get_text(strip=True) if title_a else ''
    
    modal = title_td.find(class_='modal')
    fields = {}
    if modal:
        modal_table = modal.find('table')
        if modal_table:
            for tr in modal_table.find_all('tr'):
                th = tr.find('th')
                td = tr.find('td')
                if th and td:
                    label = th.get_text(strip=True)
                    if 'Description' in label:
                        desc_div = td.find(class_='style-2')
                        fields['Description'] = desc_div.decode_contents().strip() if desc_div else td.decode_contents().strip()
                    else:
                        fields[label] = td.get_text(strip=True)

    dept = fields.get('Department', org).strip()
    desc = fields.get('Description', '').strip()
    
    youtube_td = None
    dataset_td = None
    contact_td = None
    if modal and modal.find('table'):
        for tr in modal.find('table').find_all('tr'):
            th = tr.find('th')
            td = tr.find('td')
            if th and td:
                l = th.get_text(strip=True)
                if 'Youtube' in l:
                    youtube_td = td.decode_contents().strip()
                elif 'Dataset' in l:
                    dataset_td = td.decode_contents().strip()
                elif 'Contact' in l:
                    contact_td = td.decode_contents().strip()

    youtube_link = youtube_td if youtube_td and youtube_td != '<a href=" " target="_blank"> </a>' else '<span class="text-muted">N/A</span>'
    dataset_link = dataset_td if dataset_td and dataset_td.strip() != '' else '<span class="text-muted">N/A</span>'
    contact_info = contact_td if contact_td and contact_td != '<a href=" " target="_blank"> </a>' else '<span class="text-muted">N/A</span>'

    ps_data_list.append({
        'id': f"PS_{ps_number.replace(' ', '_')}_{idx+1}",
        'sno': sno,
        'org': org,
        'title': title,
        'category': category,
        'ps_number': ps_number,
        'theme': theme,
        'department': dept,
        'description': desc,
        'youtube_link': youtube_link,
        'dataset_link': dataset_link,
        'contact_info': contact_info
    })

print(f"Successfully parsed {len(ps_data_list)} problem statements.")

clean_html_structure = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no, maximum-scale=1.0, user-scalable=no">
    <title>Smart India Hackathon - Problem Statements Directory</title>

    <!-- Dependencies -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap">

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>

    <style>
    html, body {
        width: 100%;
        max-width: 100%;
        overflow-x: hidden !important;
        font-family: 'Poppins', sans-serif;
        background-color: #f8fafc;
        color: #334155;
        padding-top: 15px;
        padding-bottom: 40px;
    }

    .container-fluid {
        width: 100%;
        max-width: 100%;
        padding-left: 12px !important;
        padding-right: 12px !important;
    }

    /* Preloader Overlay */
    .preloader-spinner {
        width: 65px;
        height: 65px;
        border: 5px solid rgba(56, 189, 248, 0.15);
        border-top-color: #38bdf8;
        border-radius: 50%;
        animation: loaderSpin 0.85s linear infinite;
    }

    @keyframes loaderSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes heartPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.25); }
    }

    /* Dashboard Header */
    .ps-dashboard-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 16px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
    }

    .ps-stat-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 8px 14px;
        text-align: center;
        flex: 1;
        min-width: 90px;
    }

    .ps-stat-value {
        font-size: 20px;
        font-weight: 800;
        line-height: 1.2;
    }

    .ps-stat-label {
        font-size: 10.5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.85;
    }

    /* Controls Panel */
    .ps-controls-panel {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .ps-filter-btn {
        border-radius: 20px;
        font-weight: 600;
        font-size: 11.5px;
        padding: 6px 12px;
        transition: all 0.2s ease;
        flex: 1;
    }

    .ps-action-btn {
        border-radius: 6px;
        font-weight: 600;
        font-size: 11.5px;
        padding: 6px 12px;
        transition: all 0.2s ease;
        flex: 1;
    }

    /* Table Container */
    .table-responsive-card {
        width: 100%;
        max-width: 100%;
        overflow-x: hidden;
    }

    #dataTablePS {
        width: 100%;
        max-width: 100%;
        border-collapse: separate !important;
        border-spacing: 0;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    #dataTablePS thead th {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        color: #f8fafc !important;
        font-weight: 700 !important;
        font-size: 12.5px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 12px 10px !important;
        border: none !important;
    }

    .ps-main-row {
        transition: background-color 0.15s ease;
        cursor: pointer;
    }

    .ps-main-row:hover {
        background-color: #f1f5f9 !important;
    }

    .ps-main-row.is-read {
        background-color: #f0fdf4 !important;
    }

    .ps-main-row.is-read:hover {
        background-color: #dcfce7 !important;
    }

    .ps-meta-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 12px;
        display: inline-flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 6px;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.03);
    }

    .badge-cat-software {
        background-color: #e0e7ff !important;
        color: #3730a3 !important;
        border: 1px solid #c7d2fe;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
    }

    .badge-cat-hardware {
        background-color: #ccfbf1 !important;
        color: #115e59 !important;
        border: 1px solid #99f6e4;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
    }

    .badge-ps-id {
        background: #0284c7;
        color: #ffffff;
        font-weight: 700;
        font-size: 11.5px;
        padding: 4px 10px;
        border-radius: 6px;
    }

    .badge-theme {
        background: #ffffff;
        color: #334155;
        border: 1px solid #cbd5e1;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
    }

    .btn-toggle-row, .btn-read-toggle {
        font-weight: 600 !important;
        font-size: 12px !important;
        padding: 6px 14px !important;
        border-radius: 6px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }

    .btn-read-toggle {
        border-radius: 20px !important;
    }

    .btn-copy-icon {
        background: transparent;
        border: none;
        color: #64748b;
        padding: 2px 5px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 11.5px;
        transition: all 0.15s ease;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    .btn-copy-icon:hover {
        background: #e2e8f0;
        color: #0284c7;
    }

    .btn-copy-btn {
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        transition: all 0.15s ease;
    }

    .ps-detail-row {
        background-color: #f8fafc !important;
    }

    .ps-detail-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #0284c7;
        border-radius: 10px;
        padding: 18px;
        margin: 6px 0 12px 0;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.07);
    }

    .ps-detail-title {
        font-size: 15.5px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.45;
        margin-bottom: 10px;
    }

    .ps-desc-container {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px;
        max-height: 340px;
        overflow-y: auto;
        font-size: 13px;
        line-height: 1.65;
        color: #334155;
    }

    .ps-pagination-bar {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 12px 16px;
        margin-top: 16px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* MOBILE CARD TRANSFORMATIONS (< 768px Phones & Tablets) */
    @media (max-width: 767.98px) {
        body {
            padding-top: 10px;
            padding-bottom: 25px;
        }

        .ps-dashboard-header {
            padding: 16px;
            text-align: center;
        }

        .ps-dashboard-header .d-flex {
            justify-content: center !important;
            margin-top: 12px;
            width: 100%;
        }

        /* Convert Table elements to Block Cards on mobile */
        #dataTablePS {
            display: block !important;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        #dataTablePS thead {
            display: none !important;
        }

        #dataTablePS tbody {
            display: block !important;
            width: 100% !important;
        }

        /* Main Row turns into a standalone Mobile Card */
        #dataTablePS tr.ps-main-row {
            display: block !important;
            width: 100% !important;
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
            margin-bottom: 12px !important;
            padding: 14px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04) !important;
            position: relative;
        }

        #dataTablePS tr.ps-main-row td {
            display: block !important;
            width: 100% !important;
            border: none !important;
            padding: 4px 0 !important;
            text-align: left !important;
        }

        #dataTablePS tr.ps-main-row td:first-child {
            display: inline-block !important;
            width: auto !important;
            background: #e2e8f0;
            color: #475569;
            font-size: 11px;
            padding: 2px 8px !important;
            border-radius: 12px;
            margin-bottom: 6px;
        }

        #dataTablePS tr.ps-main-row td:first-child::before {
            content: "S.No: #";
        }

        .ps-meta-box {
            width: 100% !important;
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 6px !important;
            margin-top: 6px;
        }

        .action-status-cell {
            padding-top: 10px !important;
            border-top: 1px dashed #e2e8f0 !important;
            margin-top: 8px !important;
        }

        .action-status-cell .d-flex {
            flex-direction: row !important;
            gap: 8px !important;
            width: 100% !important;
        }

        .btn-toggle-row, .btn-read-toggle {
            flex: 1 !important;
            width: 100% !important;
            font-size: 11.5px !important;
            padding: 8px 10px !important;
        }

        /* Detail Row Container on Mobile without !important display block so jQuery inline hide works */
        #dataTablePS tr.ps-detail-row {
            display: block;
            width: 100%;
            box-sizing: border-box;
        }

        #dataTablePS tr.ps-detail-row > td {
            display: block;
            width: 100%;
            padding: 0;
            border: none;
        }

        .ps-detail-card {
            margin: 0 0 16px 0 !important;
            border-radius: 10px !important;
            padding: 14px !important;
        }

        .ps-pagination-bar {
            flex-direction: column !important;
            text-align: center !important;
        }

        .pagination {
            justify-content: center !important;
            width: 100% !important;
        }
    }
    </style>
</head>
<body>

<!-- Preloader Screen -->
<div id="sitePreloader" style="
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    z-index: 999999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    transition: opacity 0.6s ease, visibility 0.6s ease;
">
    <div class="preloader-spinner mb-4"></div>
    <h2 style="font-weight: 800; font-size: 24px; letter-spacing: -0.5px; margin-bottom: 6px; color: #f8fafc; text-align: center;">
        Smart India Hackathon
    </h2>
    <p style="font-size: 13.5px; opacity: 0.85; margin-bottom: 20px; text-align: center; color: #38bdf8; font-weight: 600;">
        Problem Statement Directory
    </p>

    <div style="
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 9px 20px;
        border-radius: 30px;
        font-size: 12.5px;
        font-weight: 600;
        letter-spacing: 0.4px;
        color: #f1f5f9;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    ">
        <i class="fa fa-code text-info" style="color: #38bdf8 !important;"></i> Created by Dev 
        <span style="color: #64748b;">|</span> 
        <i class="fa fa-heart" style="color: #ef4444 !important; animation: heartPulse 1.2s infinite ease-in-out;"></i> Created with Love for Love
    </div>
</div>

<div class="container-fluid">

    <!-- Dashboard Header -->
    <div class="ps-dashboard-header">
        <div class="row align-items-center">
            <div class="col-md-7 text-center text-md-left mb-3 mb-md-0">
                <h3 style="margin: 0; font-weight: 800; font-size: 22px; letter-spacing: -0.5px;">
                    <i class="fa fa-cubes text-primary mr-2" style="color: #38bdf8 !important;"></i>Problem Statements Directory
                </h3>
                <p style="margin: 4px 0 0 0; opacity: 0.85; font-size: 12.5px;">
                    Mobile-responsive directory with search, status filters, and copy functionality.
                </p>
            </div>
            <div class="col-md-5">
                <div class="d-flex justify-content-center justify-content-md-end gap-2" style="gap: 10px;">
                    <div class="ps-stat-card">
                        <div class="ps-stat-value" id="statTotalCount">226</div>
                        <div class="ps-stat-label">Total</div>
                    </div>
                    <div class="ps-stat-card" style="background: rgba(34, 197, 94, 0.2); border-color: rgba(34, 197, 94, 0.4);">
                        <div class="ps-stat-value text-success" id="statReadCount" style="color: #4ade80 !important;">0</div>
                        <div class="ps-stat-label">Read</div>
                    </div>
                    <div class="ps-stat-card" style="background: rgba(245, 158, 11, 0.2); border-color: rgba(245, 158, 11, 0.4);">
                        <div class="ps-stat-value text-warning" id="statUnreadCount" style="color: #fbbf24 !important;">226</div>
                        <div class="ps-stat-label">Unread</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Controls Panel -->
    <div class="ps-controls-panel">
        <div class="row align-items-center">
            <div class="col-lg-6 col-12 mb-2 mb-lg-0">
                <div class="d-flex align-items-center flex-wrap gap-2" style="gap: 6px;">
                    <span style="font-weight: 700; font-size: 12.5px; color: #475569; margin-right: 4px;">
                        <i class="fa fa-filter text-info"></i> Status:
                    </span>
                    <button type="button" class="btn btn-primary ps-filter-btn active" id="btnFilterAll" onclick="filterReadStatus('all')">
                        All (226)
                    </button>
                    <button type="button" class="btn btn-outline-warning ps-filter-btn" id="btnFilterUnread" onclick="filterReadStatus('unread')">
                        <i class="fa fa-circle-o"></i> Unread
                    </button>
                    <button type="button" class="btn btn-outline-success ps-filter-btn" id="btnFilterRead" onclick="filterReadStatus('read')">
                        <i class="fa fa-check-circle"></i> Read
                    </button>
                </div>
            </div>
            <div class="col-lg-6 col-12">
                <div class="d-flex align-items-center justify-content-lg-end flex-wrap gap-2" style="gap: 8px;">
                    <div class="d-flex align-items-center mr-1">
                        <span style="font-size: 11.5px; font-weight: 600; color: #64748b; margin-right: 4px;">Show:</span>
                        <select id="selectPageSize" class="custom-select custom-select-sm" onchange="changePageSize(this.value)" style="width: 75px; font-weight: 600;">
                            <option value="20" selected>20</option>
                            <option value="50">50</option>
                            <option value="100">100</option>
                            <option value="all">All</option>
                        </select>
                    </div>

                    <div class="input-group input-group-sm flex-grow-1" style="max-width: 240px;">
                        <div class="input-group-prepend">
                            <span class="input-group-text bg-white border-right-0"><i class="fa fa-search text-muted"></i></span>
                        </div>
                        <input type="text" id="inputPsSearch" class="form-control border-left-0" placeholder="Search statements..." onkeyup="performSearch()">
                    </div>
                </div>
            </div>
        </div>

        <div class="d-flex align-items-center flex-wrap gap-2 pt-2" style="gap: 6px; border-top: 1px solid #f1f5f9;">
            <button type="button" class="btn btn-outline-primary ps-action-btn" id="btnExpandAllMain" onclick="toggleAllRows(true)">
                <i class="fa fa-plus-square-o"></i> Expand All
            </button>
            <button type="button" class="btn btn-outline-secondary ps-action-btn" id="btnCollapseAllMain" onclick="toggleAllRows(false)">
                <i class="fa fa-minus-square-o"></i> Collapse All
            </button>
            <button type="button" class="btn btn-outline-info ps-action-btn" onclick="markAllAsRead(true)">
                <i class="fa fa-check-square-o"></i> Mark All Read
            </button>
            <button type="button" class="btn btn-outline-danger ps-action-btn" onclick="markAllAsRead(false)">
                <i class="fa fa-refresh"></i> Reset Read
            </button>
        </div>
    </div>

    <!-- Table Container -->
    <div class="table-responsive-card">
        <table class="table" id="dataTablePS">
            <thead>
                <tr>
                    <th style="width: 5%; text-align: center;">S.No.</th>
                    <th style="width: 20%;">Organization</th>
                    <th style="width: 35%;">Problem Statement Meta (PS Number • Category • Theme)</th>
                    <th style="width: 40%; text-align: center;">Action &amp; Read Status</th>
                </tr>
            </thead>
            <tbody id="psTableBody">
                {TBODY_ROWS}
            </tbody>
        </table>
    </div>

    <!-- Pagination Bar -->
    <div class="ps-pagination-bar" id="paginationBar">
        <div id="paginationInfo" style="font-size: 12.5px; font-weight: 600; color: #475569;">
            Showing 1 to 20 of 226 entries
        </div>
        <ul class="pagination pagination-sm m-0" id="paginationNav">
            <!-- Dynamic Pagination Links -->
        </ul>
    </div>

</div>

<!-- JavaScript Controls -->
<script>
var READ_STORAGE_KEY = 'sih_read_problem_statements_v1';
var currentFilter = 'all';
var currentPage = 1;
var pageSize = 20;

// Preloader Dismissal
function hidePreloader() {
    var loader = document.getElementById('sitePreloader');
    if (loader) {
        loader.style.opacity = '0';
        loader.style.pointerEvents = 'none';
        setTimeout(function() {
            if (loader && loader.parentNode) {
                loader.parentNode.removeChild(loader);
            }
        }, 600);
    }
}

$(document).ready(function() {
    setTimeout(hidePreloader, 600);
});
window.addEventListener('load', function() {
    setTimeout(hidePreloader, 400);
});

// Clipboard Copy Functions
function copyTextDirect(text, event) {
    if (event) event.stopPropagation();
    if (!text) return;

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text);
    } else {
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
        } catch (err) {}
        document.body.removeChild(textArea);
    }

    showCopyFeedback(event);
}

function copyElementText(elementId, event) {
    if (event) event.stopPropagation();
    var elem = document.getElementById(elementId);
    if (!elem) return;
    var text = elem.innerText || elem.textContent;
    copyTextDirect(text, event);
}

function showCopyFeedback(event) {
    if (!event || !event.currentTarget) return;
    var btn = $(event.currentTarget);
    var originalHtml = btn.html();
    
    btn.html('<i class="fa fa-check text-success"></i> Copied!');
    setTimeout(function() {
        btn.html(originalHtml);
    }, 1400);
}

function getReadList() {
    try {
        var stored = localStorage.getItem(READ_STORAGE_KEY);
        return stored ? JSON.parse(stored) : [];
    } catch(e) {
        return [];
    }
}

function saveReadList(list) {
    try {
        localStorage.setItem(READ_STORAGE_KEY, JSON.stringify(list));
    } catch(e) {}
}

function updateCountsAndUI() {
    var readList = getReadList();
    var totalCount = $('.ps-main-row').length;
    var readCount = readList.length;
    var unreadCount = totalCount - readCount;

    $('#statTotalCount').text(totalCount);
    $('#statReadCount').text(readCount);
    $('#statUnreadCount').text(unreadCount);

    $('.ps-main-row').each(function() {
        var psId = $(this).attr('data-ps-id');
        var isRead = readList.indexOf(psId) !== -1;
        var btn = $('.btn-read-' + psId);

        if (isRead) {
            $(this).addClass('is-read');
            btn.removeClass('btn-outline-success').addClass('btn-success');
            btn.find('.icon-read').removeClass('fa-circle-o').addClass('fa-check-circle');
            btn.find('.read-text').text('Read ✓');
        } else {
            $(this).removeClass('is-read');
            btn.removeClass('btn-success').addClass('btn-outline-success');
            btn.find('.icon-read').removeClass('fa-check-circle').addClass('fa-circle-o');
            btn.find('.read-text').text('Mark Read');
        }
    });
}

function toggleReadState(psId, event) {
    if (event) event.stopPropagation();
    var readList = getReadList();
    var idx = readList.indexOf(psId);

    if (idx === -1) {
        readList.push(psId);
    } else {
        readList.splice(idx, 1);
    }

    saveReadList(readList);
    updateCountsAndUI();
    applyFilterAndSearch();
}

function markAllAsRead(status) {
    var list = [];
    if (status) {
        $('.ps-main-row').each(function() {
            list.push($(this).attr('data-ps-id'));
        });
    }
    saveReadList(list);
    updateCountsAndUI();
    applyFilterAndSearch();
}

function toggleSingleRow(psId, event) {
    if (event) event.stopPropagation();
    var detailRow = $('#row_detail_' + psId);
    var mainRow = $('#row_main_' + psId);
    var btn = mainRow.find('.btn-toggle-row');

    if (detailRow.is(':visible')) {
        detailRow.hide();
        btn.find('.icon-arrow').removeClass('fa-chevron-up').addClass('fa-chevron-down');
        btn.find('.btn-text').text('Expand Details');
        btn.removeClass('btn-secondary').addClass('btn-outline-primary');
    } else {
        detailRow.show();
        btn.find('.icon-arrow').removeClass('fa-chevron-down').addClass('fa-chevron-up');
        btn.find('.btn-text').text('Collapse Details');
        btn.removeClass('btn-outline-primary').addClass('btn-secondary');
    }
}

function toggleAllRows(expand) {
    $('.ps-main-row').each(function() {
        if ($(this).is(':visible')) {
            var psId = $(this).attr('data-ps-id');
            var detailRow = $('#row_detail_' + psId);
            var btn = $(this).find('.btn-toggle-row');

            if (expand) {
                detailRow.show();
                btn.find('.icon-arrow').removeClass('fa-chevron-down').addClass('fa-chevron-up');
                btn.find('.btn-text').text('Collapse Details');
                btn.removeClass('btn-outline-primary').addClass('btn-secondary');
            } else {
                detailRow.hide();
                btn.find('.icon-arrow').removeClass('fa-chevron-up').addClass('fa-chevron-down');
                btn.find('.btn-text').text('Expand Details');
                btn.removeClass('btn-secondary').addClass('btn-outline-primary');
            }
        }
    });
}

function filterReadStatus(status) {
    currentFilter = status;
    currentPage = 1;
    $('.ps-filter-btn').removeClass('active btn-primary btn-warning btn-success').addClass('btn-outline-primary');

    if (status === 'all') {
        $('#btnFilterAll').addClass('active btn-primary').removeClass('btn-outline-primary');
    } else if (status === 'unread') {
        $('#btnFilterUnread').addClass('active btn-warning').removeClass('btn-outline-primary');
    } else if (status === 'read') {
        $('#btnFilterRead').addClass('active btn-success').removeClass('btn-outline-primary');
    }

    applyFilterAndSearch();
}

function performSearch() {
    currentPage = 1;
    applyFilterAndSearch();
}

function changePageSize(val) {
    pageSize = val === 'all' ? 999999 : parseInt(val);
    currentPage = 1;
    applyFilterAndSearch();
}

function goToPage(page) {
    currentPage = page;
    applyFilterAndSearch();
    $('html, body').animate({ scrollTop: $('#dataTablePS').offset().top - 120 }, 200);
}

function applyFilterAndSearch() {
    var readList = getReadList();
    var query = ($('#inputPsSearch').val() || '').toLowerCase().trim();

    var matchingRows = [];

    $('.ps-main-row').each(function() {
        var psId = $(this).attr('data-ps-id');
        var isRead = readList.indexOf(psId) !== -1;
        var detailRow = $('#row_detail_' + psId);
        
        var matchesStatus = true;
        if (currentFilter === 'unread' && isRead) matchesStatus = false;
        if (currentFilter === 'read' && !isRead) matchesStatus = false;

        var textContent = ($(this).text() + ' ' + detailRow.text()).toLowerCase();
        var matchesQuery = query === '' || textContent.indexOf(query) !== -1;

        if (matchesStatus && matchesQuery) {
            matchingRows.push({ main: $(this), detail: detailRow });
        } else {
            $(this).hide();
            detailRow.hide();
        }
    });

    var totalMatching = matchingRows.length;
    var totalPages = Math.ceil(totalMatching / (pageSize || 1)) || 1;
    if (currentPage > totalPages) currentPage = totalPages;
    if (currentPage < 1) currentPage = 1;

    var startIdx = (currentPage - 1) * pageSize;
    var endIdx = startIdx + pageSize;

    for (var i = 0; i < totalMatching; i++) {
        var pair = matchingRows[i];
        if (i >= startIdx && i < endIdx) {
            pair.main.show();
            var isExpanded = pair.main.find('.btn-toggle-row .btn-text').text() === 'Collapse Details';
            if (isExpanded) {
                pair.detail.show();
            } else {
                pair.detail.hide();
            }
        } else {
            pair.main.hide();
            pair.detail.hide();
        }
    }

    renderPaginationControls(totalMatching, totalPages, startIdx, endIdx);
}

function renderPaginationControls(totalMatching, totalPages, startIdx, endIdx) {
    var displayStart = totalMatching === 0 ? 0 : startIdx + 1;
    var displayEnd = endIdx > totalMatching ? totalMatching : endIdx;

    $('#paginationInfo').text('Showing ' + displayStart + ' to ' + displayEnd + ' of ' + totalMatching + ' entries');

    var navHtml = '';

    // Previous Button
    navHtml += '<li class="page-item ' + (currentPage === 1 ? 'disabled' : '') + '">';
    navHtml += '<a class="page-link" href="#" onclick="goToPage(' + (currentPage - 1) + '); return false;">&laquo; Prev</a>';
    navHtml += '</li>';

    // Page Numbers
    var startPage = Math.max(1, currentPage - 2);
    var endPage = Math.min(totalPages, currentPage + 2);

    for (var p = startPage; p <= endPage; p++) {
        navHtml += '<li class="page-item ' + (p === currentPage ? 'active' : '') + '">';
        navHtml += '<a class="page-link" href="#" onclick="goToPage(' + p + '); return false;">' + p + '</a>';
        navHtml += '</li>';
    }

    // Next Button
    navHtml += '<li class="page-item ' + (currentPage === totalPages ? 'disabled' : '') + '">';
    navHtml += '<a class="page-link" href="#" onclick="goToPage(' + (currentPage + 1) + '); return false;">Next &raquo;</a>';
    navHtml += '</li>';

    $('#paginationNav').html(navHtml);
}

$(document).ready(function() {
    updateCountsAndUI();
    applyFilterAndSearch();

    $('.ps-main-row').on('click', function(e) {
        if ($(e.target).closest('button').length === 0 && $(e.target).closest('a').length === 0) {
            var psId = $(this).attr('data-ps-id');
            toggleSingleRow(psId, e);
        }
    });
});
</script>

</body>
</html>
'''

# Build Table Rows
new_tbody_rows = []

for item in ps_data_list:
    ps_id = item['id']
    sno = item['sno']
    org = item['org']
    cat = item['category']
    cat_class = "badge-cat-hardware" if "Hardware" in cat else "badge-cat-software"
    ps_num = item['ps_number']
    theme = item['theme']
    title = item['title']
    dept = item['department']
    desc = item['description']
    yt = item['youtube_link']
    ds = item['dataset_link']
    contact = item['contact_info']
    
    escaped_title = html.escape(title).replace("'", "\\'").replace('"', '&quot;').replace('\n', ' ')
    escaped_org = html.escape(org).replace("'", "\\'").replace('"', '&quot;').replace('\n', ' ')
    escaped_ps_num = html.escape(ps_num).replace("'", "\\'").replace('"', '&quot;')
    escaped_theme = html.escape(theme).replace("'", "\\'").replace('"', '&quot;')
    escaped_dept = html.escape(dept).replace("'", "\\'").replace('"', '&quot;')
    
    meta_box_html = f'''
    <div class="ps-meta-box">
        <span class="badge badge-ps-id">
            <i class="fa fa-tag"></i> {ps_num}
            <button type="button" class="btn-copy-icon" style="color: #ffffff; opacity: 0.9;" onclick="copyTextDirect('{escaped_ps_num}', event)" title="Copy PS Number">
                <i class="fa fa-clone"></i>
            </button>
        </span>
        <span class="badge {cat_class}">
            {cat}
        </span>
        <span class="badge badge-theme">
            <i class="fa fa-bookmark-o"></i> {theme}
            <button type="button" class="btn-copy-icon" onclick="copyTextDirect('{escaped_theme}', event)" title="Copy Theme">
                <i class="fa fa-clone"></i>
            </button>
        </span>
    </div>
    '''
    
    main_tr = f'''
    <tr id="row_main_{ps_id}" class="ps-main-row" data-ps-id="{ps_id}">
        <td class="colomn_border text-center font-weight-bold" style="vertical-align: middle;">{sno}</td>
        <td class="colomn_border" style="vertical-align: middle; font-size: 13.5px; font-weight: 600; color: #1e293b;">
            {org}
            <button type="button" class="btn-copy-icon" onclick="copyTextDirect('{escaped_org}', event)" title="Copy Organization">
                <i class="fa fa-clone"></i>
            </button>
        </td>
        <td class="colomn_border" style="vertical-align: middle;">
            {meta_box_html}
        </td>
        <td class="colomn_border text-center action-status-cell" style="vertical-align: middle;">
            <div class="d-flex align-items-center justify-content-center flex-wrap" style="gap: 10px;">
                <button type="button" class="btn btn-secondary btn-toggle-row" onclick="toggleSingleRow('{ps_id}', event)">
                    <i class="fa fa-chevron-up icon-arrow"></i> <span class="btn-text">Collapse Details</span>
                </button>
                <button type="button" class="btn btn-outline-success btn-read-toggle btn-read-{ps_id}" onclick="toggleReadState('{ps_id}', event)">
                    <i class="fa fa-circle-o icon-read"></i> <span class="read-text">Mark Read</span>
                </button>
            </div>
        </td>
    </tr>
    <tr id="row_detail_{ps_id}" class="ps-detail-row" data-ps-id="{ps_id}">
        <td colspan="4" style="padding: 0 14px 14px 14px; border-top: none;">
            <div class="ps-detail-card">
                <div class="d-flex justify-content-between align-items-start mb-2 pb-2" style="border-bottom: 1px solid #e2e8f0;">
                    <div>
                        <div class="ps-detail-title">
                            <i class="fa fa-file-text-o text-primary mr-2" style="color: #0284c7 !important;"></i>
                            {title}
                            <button type="button" class="btn btn-xs btn-outline-secondary btn-copy-btn ml-2" onclick="copyTextDirect('{escaped_title}', event)">
                                <i class="fa fa-clone"></i> Copy Title
                            </button>
                        </div>
                    </div>
                    <div class="d-flex align-items-center gap-2" style="gap: 8px;">
                        <span class="badge badge-info" style="font-size: 12px; padding: 6px 12px;">PS ID: {ps_num}</span>
                        <span class="badge {cat_class}">{cat}</span>
                    </div>
                </div>
                
                <div class="mb-3">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <strong style="color: #0f172a; font-size: 13px;">
                            <i class="fa fa-align-left text-info"></i> Full Description &amp; Requirements:
                        </strong>
                        <button type="button" class="btn btn-xs btn-outline-secondary btn-copy-btn" onclick="copyElementText('desc_container_{ps_id}', event)">
                            <i class="fa fa-clone"></i> Copy Description
                        </button>
                    </div>
                    <div class="ps-desc-container style-2" id="desc_container_{ps_id}">
                        {desc}
                    </div>
                </div>

                <div class="row" style="font-size: 12.5px; color: #475569; background: #f1f5f9; padding: 12px; border-radius: 8px; margin: 0;">
                    <div class="col-md-6 mb-1">
                        <strong><i class="fa fa-building-o text-secondary"></i> Department:</strong> {dept}
                        <button type="button" class="btn-copy-icon" onclick="copyTextDirect('{escaped_dept}', event)" title="Copy Department">
                            <i class="fa fa-clone"></i>
                        </button>
                    </div>
                    <div class="col-md-6 mb-1">
                        <strong><i class="fa fa-sitemap text-secondary"></i> Organization:</strong> {org}
                        <button type="button" class="btn-copy-icon" onclick="copyTextDirect('{escaped_org}', event)" title="Copy Organization">
                            <i class="fa fa-clone"></i>
                        </button>
                    </div>
                    <div class="col-md-4 mb-1">
                        <strong><i class="fa fa-youtube-play text-danger"></i> YouTube Link:</strong> {yt}
                    </div>
                    <div class="col-md-4 mb-1">
                        <strong><i class="fa fa-database text-warning"></i> Dataset Link:</strong> {ds}
                    </div>
                    <div class="col-md-4 mb-1">
                        <strong><i class="fa fa-address-book-o text-success"></i> Contact Info:</strong> {contact}
                    </div>
                </div>
            </div>
        </td>
    </tr>
    '''
    new_tbody_rows.append(main_tr)

# Inject rows into clean HTML structure
final_html = clean_html_structure.replace('{TBODY_ROWS}', ''.join(new_tbody_rows))

print("Writing phone expand/collapse fix index.html...")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Phone Expand/Collapse fix complete!")
