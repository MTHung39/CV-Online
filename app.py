from flask import Flask, render_template, send_file, url_for
import pdfkit
import os
import tempfile
import json

# Cấu hình wkhtmltopdf
path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

app = Flask(__name__)

# Đọc dữ liệu từ JSON
with open('cv_data.json', encoding='utf-8') as f:
    cv_data = json.load(f)

@app.route('/')
def home():
    return render_template('index.html', cv=cv_data)

@app.route('/projects')
def projects():
    project_list = [
        {
            'name': 'Note App',
            'description': 'Một ứng dụng ghi chú đơn giản nhưng mạnh mẽ',
            'link': 'https://github.com/MTHung39/note_app'
        },
        {
            'name': 'BMI Calculator',
            'description': 'Ứng dụng tính chỉ số BMI có giao diện trực quan, lưu lịch sử, hiển thị biểu đồ.',
            'link': 'https://github.com/MTHung39/bmi-calculator'
        },
    ]
    return render_template('projects.html', projects=project_list)

@app.route('/download_cv')
def download_cv():
    # Tạo HTML tạm thời có đường dẫn tuyệt đối
    rendered = render_template('index.html', cv=cv_data)

    # Ghi vào file HTML tạm
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as temp_html:
        temp_html.write(rendered)
        temp_html_path = temp_html.name

    # Cấu hình tùy chọn PDF
    options = {
        'enable-local-file-access': None,
        'encoding': "UTF-8",
        'quiet': ''
    }

    # Tạo file PDF tạm
    pdf_fd, pdf_path = tempfile.mkstemp(suffix='.pdf')
    os.close(pdf_fd)

    pdfkit.from_file(temp_html_path, pdf_path, configuration=config, options=options)

    # Gửi file PDF cho người dùng
    return send_file(pdf_path, as_attachment=True, download_name='cv.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

