from flask import Flask, render_template, send_file, url_for, request
from weasyprint import HTML
import os
import tempfile
import json
import io

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
    cv_html = render_template('index.html', cv=cv_data)
    pdf = HTML(string=cv_html, base_url=request.url_root).write_pdf()
    return send_file(io.BytesIO(pdf), as_attachment=True, download_name='cv.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

