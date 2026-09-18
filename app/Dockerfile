# استخدام صورة بايثون خفيفة ورسمية
FROM python:3.11-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كود التطبيق
COPY app.py .

# فتح المنفذ الخاص بالتطبيق
EXPOSE 5000

# أمر تشغيل التطبيق عند بدء الحاوية
CMD ["python", "app.py"]
