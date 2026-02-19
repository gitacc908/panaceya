from django.core.management.base import BaseCommand

from marketing.models import (
    ContactLink,
    ContactsPage,
    DepositForum,
    DepositsPage,
    ExampleLink,
    FaqItem,
    FaqPage,
    FeatureBlock,
    HomePage,
    RoadmapItem,
    RoadmapPage,
    ServiceItem,
    ServicesPage,
)


class Command(BaseCommand):
    help = "Создаёт дефолтные данные для marketing"

    def handle(self, *args, **options):
        homepage, _ = HomePage.objects.get_or_create(
            pk=1,
            defaults={
                "hero_title": "ПАНАЦЕЯ - СЕРВИС РЕШЕНИЯ ВСЕХ ПРОБЛЕМ ВАШЕГО БИЗНЕСА",
                "hero_subtitle": "САМАЯ ВЫГОДНАЯ И ФУНКЦИОНАЛЬНЯ АВТОМАТИЗАЦИЯ НА РЫНКЕ",
                "hero_cta_text": "СОЗДАЙ БЕСПЛАТНЫЙ САЙТ И БОТА ДЛЯ АВТОМАТИЗАЦИИ СВОИХ МАГАЗИНОВ",
                "available_currencies": "Доступные валюты: uah, rub, kzt, $",
                "features_title": "Преимущества",
                "example_sites_title": "Примеры сайтов",
                "example_bots_title": "Примеры ботов",
            },
        )

        contacts_page, _ = ContactsPage.objects.get_or_create(
            pk=1,
            defaults={
                "title": "Контакты",
                "description": "Свяжитесь с менеджером или технической поддержкой.",
                "telegram_channel_url": "https://t.me/example_channel",
            },
        )

        features = [
            {
                "title": "Быстрое подключение",
                "text": "Запускаем ваш проект в короткие сроки и сопровождаем на каждом этапе.",
            },
            {
                "title": "Поддержка управления сетью магазинов",
                "text": "Вы можете держать в одной панели все свои магазины и управлять ими централизованно.",
            },
            {
                "title": "Автоматизация курьеров и подсчет их дохода",
                "text": "Курьеры могут сами добавлять товар, а система автоматически считает доход и отчётность.",
            },
            {
                "title": "Защита от сносов и ддос атак",
                "text": "Современная защита от ддос и других рисков для стабильной работы проекта.",
            },
            {
                "title": "Уникальная система скидок",
                "text": "Гибкие механики скидок и персональные условия для разных категорий клиентов.",
            },
            {
                "title": "Проработанная статистика",
                "text": "Детальная аналитика по продажам, эффективности и ключевым показателям.",
            },
            {
                "title": "Развивающийся проект",
                "text": "Мы регулярно публикуем обновления и новости о развитии системы.",
                "use_telegram_channel_link": True,
                "telegram_link_label": "Ссылка на канал в разделе контакты",
            },
            {
                "title": "Бесплатная система",
                "text": "Клиенты платят за вас комиссию, что снижает вашу операционную нагрузку.",
            },
        ]

        for index, data in enumerate(features, start=1):
            FeatureBlock.objects.get_or_create(
                title=data["title"],
                defaults={
                    "text": data["text"],
                    "order": index,
                    "show_on_home": True,
                    "use_telegram_channel_link": data.get("use_telegram_channel_link", False),
                    "telegram_link_label": data.get("telegram_link_label", ""),
                },
            )

        for index, (link_type, title, url) in enumerate(
            [
                (ExampleLink.SITE, "Пример сайта 1", "https://example.com/site-1"),
                (ExampleLink.SITE, "Пример сайта 2", "https://example.com/site-2"),
                (ExampleLink.BOT, "Пример бота 1", "https://t.me/example_bot_1"),
                (ExampleLink.BOT, "Пример бота 2", "https://t.me/example_bot_2"),
            ],
            start=1,
        ):
            ExampleLink.objects.get_or_create(
                link_type=link_type,
                title=title,
                defaults={"url": url, "order": index},
            )

        ContactLink.objects.get_or_create(
            role=ContactLink.MANAGER,
            title="Менеджер",
            defaults={
                "url": "https://t.me/example_manager",
                "description": "Вопросы подключения и запуска",
                "order": 1,
            },
        )
        ContactLink.objects.get_or_create(
            role=ContactLink.SUPPORT,
            title="Техническая поддержка",
            defaults={
                "url": "https://t.me/example_support",
                "description": "Технические вопросы и помощь",
                "order": 2,
            },
        )

        deposits_page, _ = DepositsPage.objects.get_or_create(
            pk=1,
            defaults={
                "title": "Депозиты",
                "big_text": "Ниже размещена информация о текущих депозитах и размещениях на форумах.",
                "total_deposits": "1 000 000$",
            },
        )

        for index, forum in enumerate(
            [
                ("Forum Alpha", "https://example.com/forum-alpha", "250 000$"),
                ("Forum Beta", "https://example.com/forum-beta", "350 000$"),
            ],
            start=1,
        ):
            DepositForum.objects.get_or_create(
                page=deposits_page,
                forum_name=forum[0],
                defaults={
                    "forum_url": forum[1],
                    "deposit_amount": forum[2],
                    "order": index,
                },
            )

        RoadmapPage.objects.get_or_create(
            pk=1,
            defaults={
                "title": "Roadmap",
                "intro_text": "Ближайшие этапы развития платформы.",
            },
        )

        for index, item in enumerate(
            [
                ("Релиз обновлённой панели", "Новый интерфейс управления магазинами.", "В работе"),
                ("Расширение интеграций", "Добавление новых платёжных и сервисных интеграций.", "План"),
                ("Новая аналитика", "Расширенные отчёты и экспорт данных.", "План"),
            ],
            start=1,
        ):
            RoadmapItem.objects.get_or_create(
                title=item[0],
                defaults={
                    "description": item[1],
                    "status_label": item[2],
                    "order": index,
                },
            )

        ServicesPage.objects.get_or_create(
            pk=1,
            defaults={
                "title": "Услуги",
                "intro_text": "Список доступных услуг платформы.",
            },
        )

        ServiceItem.objects.get_or_create(title="Услуга 1", defaults={"description": "Описание услуги 1", "order": 1})
        ServiceItem.objects.get_or_create(title="Услуга 2", defaults={"description": "Описание услуги 2", "order": 2})

        FaqPage.objects.get_or_create(
            pk=1,
            defaults={
                "title": "FAQ",
                "intro_text": "Обязательные требования системы для начала работы.",
            },
        )

        FaqItem.objects.get_or_create(
            question="Магазинам с оборотом от 1000$ в день даем в пользование сайт с вашим названием",
            defaults={"answer": "Условия предоставляются после проверки оборота.", "order": 1},
        )
        FaqItem.objects.get_or_create(
            question="Мы храним данные не активных магазинов только 6 месяцев",
            defaults={"answer": "После этого срока данные архивируются и удаляются.", "order": 2},
        )

        self.stdout.write(self.style.SUCCESS("Дефолтные данные marketing созданы или уже существуют."))
