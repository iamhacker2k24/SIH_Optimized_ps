from bs4 import BeautifulSoup
import re

html_path = r'c:\Users\mrdeb\Desktop\html\index.html.bak'
output_path = r'c:\Users\mrdeb\Desktop\html\index.html'

print("Reading backup file...")
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

tbody = soup.find('tbody')
rows = tbody.find_all('tr', recursive=False)

print(f"Processing {len(rows)} rows...")

for idx, r in enumerate(rows):
    tds = r.find_all('td', recursive=False)
    if len(tds) < 8:
        continue
    
    title_td = tds[2]
    modal = title_td.find(class_='modal')
    if not modal:
        continue
    
    # Extract title text
    title_a = title_td.find('a')
    title_text = title_a.get_text(strip=True) if title_a else 'Problem Statement Details'
    
    # Extract fields from modal table
    modal_table = modal.find('table')
    fields = {}
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

    clean_ps_id = tds[4].get_text(strip=True)
    if not clean_ps_id:
        clean_ps_id = fields.get('Problem Statement ID', '').strip()

    category = tds[3].get_text(strip=True) or fields.get('Category', '').strip()
    theme = tds[6].get_text(strip=True) or fields.get('Theme', '').strip()
    description = fields.get('Description', '').strip()
    department = fields.get('Department', '').strip() or tds[1].get_text(strip=True)
    organization = tds[1].get_text(strip=True) or fields.get('Organization', '').strip()
    
    # Links extraction
    youtube_td = None
    dataset_td = None
    contact_td = None
    if modal_table:
        for tr in modal_table.find_all('tr'):
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

    # Build new title_td content
    new_inner_html = f'''
        <div class="ps-title-wrapper" style="margin-bottom: 6px;">
            <a class="ps-inline-toggle" style="font-size:15px; font-weight:600; color:#0d6efd; cursor:pointer; text-decoration:none;" onclick="$(this).closest('td').find('.ps-inline-details').slideToggle(200); return false;">
                <i class="fa fa-chevron-down text-muted" style="margin-right:6px; font-size:12px;"></i>
                {title_text}
            </a>
            <button type="button" class="btn btn-xs btn-outline-primary ml-2 py-0 px-2" style="font-size:11px; border-radius:12px; vertical-align:middle;" onclick="$(this).closest('td').find('.ps-inline-details').slideToggle(200);">
                <i class="fa fa-eye"></i> Details
            </button>
        </div>
        <div class="ps-inline-details" style="display:none; margin-top: 10px; padding: 16px; background-color: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">
                <span style="font-weight:700; color:#0f172a; font-size:14px;">
                    <i class="fa fa-file-text-o text-info" style="margin-right:6px;"></i> Problem Statement Details (PS ID: {clean_ps_id})
                </span>
                <span class="badge badge-info" style="font-size:12px; padding: 4px 8px;">{category} | {theme}</span>
            </div>
            <div style="margin-bottom: 12px;">
                <strong style="color: #334155; font-size: 13px; display: block; margin-bottom: 6px;">Description &amp; Requirements:</strong>
                <div class="style-2" style="background: #ffffff; padding: 12px 16px; border: 1px solid #e2e8f0; border-radius: 6px; max-height: 300px; overflow-y: auto; font-size: 13px; line-height: 1.6; color: #1e293b;">
                    {description}
                </div>
            </div>
            <div class="row" style="font-size: 12px; color: #475569;">
                <div class="col-md-6 mb-1">
                    <strong>Department:</strong> {department}
                </div>
                <div class="col-md-6 mb-1">
                    <strong>Organization:</strong> {organization}
                </div>
                <div class="col-md-4 mb-1">
                    <strong>Youtube Link:</strong> {youtube_link}
                </div>
                <div class="col-md-4 mb-1">
                    <strong>Dataset Link:</strong> {dataset_link}
                </div>
                <div class="col-md-4 mb-1">
                    <strong>Contact Info:</strong> {contact_info}
                </div>
            </div>
        </div>
    '''
    
    title_td.clear()
    title_td.append(BeautifulSoup(new_inner_html, 'html.parser'))

# Insert controls bar above #dataTablePS
table_elem = soup.find('table', id='dataTablePS')
if table_elem:
    controls_html = '''
    <div class="ps-controls-bar d-flex justify-content-between align-items-center mb-3 p-3" style="background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px;">
        <div>
            <h5 style="margin: 0; color: #0f172a; font-weight: 700; font-size: 16px;">
                <i class="fa fa-list-alt text-primary" style="margin-right: 8px;"></i> Problem Statements Directory
            </h5>
            <small class="text-muted">Click any Problem Statement title to view details inline. No popups required.</small>
        </div>
        <div>
            <button id="btnExpandAllPS" type="button" class="btn btn-sm btn-outline-primary mr-2" style="font-weight: 600;">
                <i class="fa fa-plus-square-o"></i> Expand All Details
            </button>
            <button id="btnCollapseAllPS" type="button" class="btn btn-sm btn-outline-secondary" style="font-weight: 600;">
                <i class="fa fa-minus-square-o"></i> Collapse All Details
            </button>
        </div>
    </div>
    '''
    table_elem.insert_before(BeautifulSoup(controls_html, 'html.parser'))

# Add JS handlers at body end
script_html = '''
<script>
$(document).ready(function() {
    $(document).on('click', '#btnExpandAllPS', function() {
        $('.ps-inline-details').slideDown(200);
    });
    $(document).on('click', '#btnCollapseAllPS', function() {
        $('.ps-inline-details').slideUp(200);
    });
});
</script>
'''
soup.body.append(BeautifulSoup(script_html, 'html.parser'))

print("Writing output to index.html...")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Transformation successfully finished!")
