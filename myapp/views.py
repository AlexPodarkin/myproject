import requests
from django.shortcuts import render, redirect
import logging
from . import models
from . import forms
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def index(request):
    # logger.debug('request index')
    return render(request, 'myapp/index.html')


def send_by_telegram(message_bot):
    tel_bot = os.getenv('tel_bot')
    chat_id = "1301604918"
    url = f"https://api.telegram.org/bot{tel_bot}/sendMessage?chat_id={chat_id}&text={message_bot}"
    try:
        requests.get(url).json()
        logger.debug('сообщение в телеграмм успешно отправлено')
    except ConnectionError:
        logger.error('сообщение в телеграмм НЕ отправлено!')


def make_order(request):
    addresses = models.Address.objects.all()
    if request.method == 'POST':
        form = forms.AddOrderForm(request.POST)
        if form.is_valid():
            object_order = form.save()
            # Сообщение в телеграмм
            message_bot = f'ЗАКАЗ № {object_order.pk}\n{form.cleaned_data["form_sign"]}р,' \
                          f'\nцвет таблички: {form.cleaned_data["color_sign"]},' \
                          f'\nадрес: {form.cleaned_data["address_sign"]}, ' \
                          f'\nимя заказчика: {form.cleaned_data["customer_name"]},' \
                          f'\nemail: {form.cleaned_data["customer_email"]},' \
                          f'\nтелефон:  {form.cleaned_data["customer_phone"]}'
            send_by_telegram(message_bot)
            # Сообщение на почту мне
            smtp_server = smtplib.SMTP("smtp.yandex.ru", 587)
            try:
                smtp_server.starttls()
                smtp_server.login("podarkinorders@yandex.ru", os.getenv('smtp_server'))
            except smtplib.SMTPException:
                logger.error('не удалось создать подключение к почте podarkinorders@yandex.ru')
            msg = MIMEMultipart()
            msg["From"] = "podarkinorders@yandex.ru"
            msg["To"] = "alexchembarov@gmail.com"
            msg["Subject"] = "Заказ из Магазина PodarkiN"
            # текст письма
            msg.attach(MIMEText(message_bot))
            try:
                smtp_server.sendmail("podarkinorders@yandex.ru", "alexchembarov@gmail.com", msg.as_string())
                logger.debug('отправка заказа на мою почту прошла успешно')
            except smtplib.SMTPException:
                logger.error('ошибка отправки заказа на мою почту')
            # Сообщение на почту клиента
            msg2 = MIMEMultipart()
            msg2["From"] = "podarkinorders@yandex.ru"
            msg2["To"] = f'{form.cleaned_data["customer_email"]}'
            msg2["Subject"] = "Магазин PodarkiN"
            text_client = f'Здравствуйте, {form.cleaned_data["customer_name"]} ! \n' \
                          f'Мы получили ваш заказ, в ближайшее время вышлем вам эскиз на утверждение.\n' \
                          f'По всем вопросам, можете обращаться по телефону 89270740573 (Александр).' \
                          f'\nВаш заказ № {object_order.pk} \nPodarkiN ® '
            msg2.attach(MIMEText(text_client))
            try:
                smtp_server.sendmail("podarkinorders@yandex.ru", f'{form.cleaned_data["customer_email"]}',
                                     msg2.as_string())
                logger.debug('отправка заказа на почту клиента прошла успешно')
            except smtplib.SMTPException:
                logger.error('ошибка отправки заказа на почту клиента')
            smtp_server.quit()
            # сообщение на сайт
            message = f'Ваш заказ № {object_order.pk} успешно оформлен! На почту ' \
                      f'{form.cleaned_data["customer_email"]} было выслано письмо с подтверждением заказа(если ' \
                      f'письма нет, проверьте папку "спам"), ' \
                      f'хорошего дня!'
            return render(request, 'myapp/make_order.html', {'message': message, 'addresses': addresses})
    else:
        form = forms.AddOrderForm()
    return render(request, 'myapp/make_order.html', {'form': form, 'addresses': addresses})


def our_works(request):
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/our_works/')
    else:
        form = forms.ReviewForm()
    reviews = models.Review.objects.all()
    return render(request, 'myapp/our_works.html', {'form': form, 'reviews': reviews})


def printing_on_mugs(request):
    return render(request, 'myapp/printing_on_mugs.html')


def printing_shirts(request):
    return render(request, 'myapp/printing_shirts.html')


def assortment_gifts(request):
    return render(request, 'myapp/assortment_gifts.html')


def page_not_found_view(request, exception):
    return render(request, 'myapp/404.html', status=404)
