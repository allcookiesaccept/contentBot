FEEDS = {
    "site1": {
        "without_photos": "https://api.site1.ru/files/export/site1_no_photo.xml",
        "with_photos": "https://api.site1.ru/files/export/site1_photo.xml",
        "without_description": "https://api.site1.ru/files/export/site1_no_description.xml",
        "with_description": "https://api.site1.ru/files/export/site1_description.xml",
    },
    "site2": {
        "without_photos": "https://api.site2.ru/files/export/nb_no_photo.xml",
        "with_photos": "https://api.site2.ru/files/export/nb_photo.xml",
        "without_description": "https://api.site2.ru/files/export/nb_no_description.xml",
        "with_description": "https://api.site2.ru/files/export/nb_description.xml",
    },
    "site3": {
        "without_photos": "https://api.site3.ru/files/export/b2b_no_photo.xml",
        "with_photos": "https://api.site3.ru/files/export/b2b_photo.xml",
        "without_description": "https://api.site3.ru/files/export/b2b_no_description.xml",
        "with_description": "https://api.site3.ru/files/export/b2b_description.xml",
    },
    "site4": {
        "without_photos": "https://api.site4.ru/files/export/samsung_no_photo.xml",
        "with_photos": "https://api.site4.ru/files/export/samsung_photo.xml",
        "without_description": "https://api.site4.ru/files/export/samsung_no_description.xml",
        "with_description": "https://api.site4.ru/files/export/samsung_description.xml",
    },
    "site5": {
        "without_photos": "https://api.site5.ru/files/export/sony_no_photo.xml",
        "with_photos": "https://api.site5.ru/files/export/sony_photo.xml",
        "without_description": "https://api.site5.ru/files/export/sony_no_description.xml",
        "with_description": "https://api.site5.ru/files/export/sony_description.xml",
    },
    "site6": {
        "without_photos": "https://api.site6.ru/files/site6/export/site6_no_photo.xml",
        "with_photos": "https://api.site6.ru/files/site6/export/site6_photo.xml",
        "without_description": "https://api.site6.ru/files/site6/export/site6_no_description.xml",
        "with_description": "https://api.site6.ru/files/site6/export/site6_description.xml",
    },
}
COLUMNS = {
    "site1": {
        "photo_upload": ["IE_XML_ID", "IP_PROP62"],
        "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
    },
    "site2": {
        "photo_upload": ["IE_XML_ID", "IP_PROP976"],
        "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
    },
    "site3": {
        "photo_upload": ["IE_XML_ID", "IP_PROP1989"],
        "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
    },
    "site4": {
        "photo_upload": ["IE_XML_ID", "IP_PROP3964"],
        "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
    },
    "site5": {
        "photo_upload": ["IE_XML_ID", "IP_PROP4884"],
        "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
    },
    "site6": {
        "photo_upload": ["IE_XML_ID", "IP_PROP4885"],
        "description_upload": ["IE_XML_ID", "IE_DETAIL_TEXT"],
    },
}

SITES = [
    "site1",
    "site2",
    "site3",
    "site4",
    "site5",
    "site6",
]

TASKS = [
    "Загрузить фотографии",
    "Добавить описания",
]

REPRISE = ["Почему бы и нет?", "В другой раз."]

PHOTOLESS_SITES = [f"Сайт без фото: {site}" for site in SITES]
DESCRIPTIONLESS_SITES = [f"Сайт без описаний: {site}" for site in SITES]


