from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


class AnnouncementForm(StatesGroup):
    property_type = State()
    location_type = State()
    jkh_name = State()
    region = State()
    orientir = State()
    rooms = State()
    total_floors = State()
    floor = State()
    condition = State()
    additional_features = State()
    price = State()
    contact = State()
    phone_number = State()
    custom_feature_input = State()


def property_type_buttons():
    buttons = [
        [InlineKeyboardButton(text="Квартира", callback_data="apartment")],
        [InlineKeyboardButton(text="Дом", callback_data="house")],
        [InlineKeyboardButton(text="Коммерческая", callback_data="commercial")],
        [InlineKeyboardButton(text="Участок", callback_data="land")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def location_type_buttons():
    buttons = [
        [InlineKeyboardButton(text="ЖК", callback_data="jkh")],
        [InlineKeyboardButton(text="Район", callback_data="region")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def region_buttons():
    buttons = [
        [InlineKeyboardButton(text="Чиланзар", callback_data="chilanzar")],
        [InlineKeyboardButton(text="Юнусабад", callback_data="yunusabad")],
        [InlineKeyboardButton(text="Мирабад", callback_data="mirabad")],
        [InlineKeyboardButton(text="Шайхантахур", callback_data="shaykhontokhur")],
        [InlineKeyboardButton(text="↩️ Ввести вручную", callback_data="custom_region")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def jkh_buttons():
    buttons = [
        [InlineKeyboardButton(text="ЖК NRG Oybek", callback_data="nrg_oybek")],
        [InlineKeyboardButton(text="ЖК Kamron Palace", callback_data="kamron_palace")],
        [InlineKeyboardButton(text="ЖК Central Park", callback_data="central_park")],
        [InlineKeyboardButton(text="↩️ Ввести вручную", callback_data="custom_jkh")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def rooms_buttons():
    # Create all number buttons first
    buttons = [
        InlineKeyboardButton(text=str(i), callback_data=str(i))
        for i in range(1, 12)
    ]

    # Split into chunks of 4 buttons per row
    keyboard = []
    for i in range(0, len(buttons), 4):
        row = buttons[i:i + 4]
        keyboard.append(row)

    # Add manual input button as a separate row
    keyboard.append([InlineKeyboardButton(text="↩️ Ввести вручную", callback_data="custom_rooms")])


def floor_buttons(total_floors):
    # Create buttons for each floor
    floor_buttons = [
        InlineKeyboardButton(text=str(i), callback_data=str(i))
        for i in range(1, int(total_floors) + 1)
    ]

    # Split into rows of 4 buttons each
    rows = []
    for i in range(0, len(floor_buttons), 4):
        row = floor_buttons[i:i + 4]
        rows.append(row)

    # Add manual input button as a separate row
    rows.append([InlineKeyboardButton(text="↩️ Ввести вручную", callback_data="custom_floor")])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def condition_buttons():
    buttons = [
        [InlineKeyboardButton(text="Евролюкс", callback_data="euro_lux")],
        [InlineKeyboardButton(text="Коробка", callback_data="box")],
        [InlineKeyboardButton(text="Luxury интерьер", callback_data="luxury")],
        [InlineKeyboardButton(text="Евро ремонт", callback_data="euro_repair")],
        [InlineKeyboardButton(text="Черновая отделка", callback_data="rough")],
        [InlineKeyboardButton(text="Предчистовая отделка", callback_data="pre_finish")],
        [InlineKeyboardButton(text="↩️ Ввести вручную", callback_data="custom_condition")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


ESSENTIAL_FEATURES = {
    # Construction
    "new_building": "Новостройка",
    "secondary": "Вторичное жилье",

    # Key amenities
    "wardrobe": "Гардеробная",
    "balcony": "Балкон",
    "loggia": "Лоджия",

    # Technical
    "heating": "Отопление",
    "gas": "Газ",
    "water_supply": "Водоснабжение",

    # Security
    "security": "Охрана",
    "intercom": "Домофон",

    # Outdoor
    "parking": "Парковка",
    "garage": "Гараж",

    # Comfort
    "air_conditioning": "Кондиционер",
    "wifi": "Wi-Fi",
}


def get_feature_buttons(selected_features=None, custom_features=None):
    if selected_features is None:
        selected_features = []
    if custom_features is None:
        custom_features = []

    builder = InlineKeyboardBuilder()

    # Add essential features
    for feature_id, feature_text in ESSENTIAL_FEATURES.items():
        text = f"✅ {feature_text}" if feature_id in selected_features else feature_text
        builder.button(text=text, callback_data=feature_id)

    # Add custom features
    for feature in custom_features:
        builder.button(text=f"✅ {feature}", callback_data=f"custom_{feature}")

    # Add action buttons
    builder.button(text="✏️ Добавить свою", callback_data="add_custom")
    builder.button(text="✔️ Готово", callback_data="done")

    builder.adjust(2)  # 2 buttons per row
    return builder.as_markup()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать! Давайте создадим ваше объявление для продажи недвижимости.\n\n"
        "Какую недвижимость вы продаете?",
        reply_markup=property_type_buttons()
    )
    await state.set_state(AnnouncementForm.property_type)


@router.callback_query(AnnouncementForm.property_type)
async def process_property_type(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(property_type=callback.data)
    await callback.message.edit_text("Это ЖК или Район?", reply_markup=location_type_buttons())
    await state.set_state(AnnouncementForm.location_type)
    await callback.answer()


@router.callback_query(AnnouncementForm.location_type)
async def process_location_type(callback: types.CallbackQuery, state: FSMContext):
    location_type = callback.data
    await state.update_data(location_type=location_type)

    if location_type == "jkh":
        await callback.message.edit_text(
            "Выберите ЖК из списка или введите свой вариант:",
            reply_markup=jkh_buttons()
        )
        await state.set_state(AnnouncementForm.jkh_name)
    else:
        await callback.message.edit_text(
            "Выберите район из списка или введите свой вариант:",
            reply_markup=region_buttons()
        )
        await state.set_state(AnnouncementForm.region)

    await callback.answer()


@router.callback_query(AnnouncementForm.jkh_name)
async def process_jkh_name(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "custom_jkh":
        await callback.message.edit_text("Введите название ЖК:")
    else:
        await state.update_data(jkh_name=callback.data)
        await callback.message.edit_text("Укажите ориентир (например: Ойбек, Мирабадский район):")
        await state.set_state(AnnouncementForm.orientir)
    await callback.answer()


@router.message(AnnouncementForm.jkh_name)
async def process_custom_jkh(message: Message, state: FSMContext):
    await state.update_data(jkh_name=message.text)
    await message.answer("Укажите ориентир (например: Ойбек, Мирабадский район):")
    await state.set_state(AnnouncementForm.orientir)


@router.callback_query(AnnouncementForm.region)
async def process_region(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "custom_region":
        await callback.message.edit_text("Введите название района:")
    else:
        await state.update_data(region=callback.data)
        await callback.message.edit_text("Укажите ориентир (например: Ойбек, Мирабадский район):")
        await state.set_state(AnnouncementForm.orientir)
    await callback.answer()


@router.message(AnnouncementForm.region)
async def process_custom_region(message: Message, state: FSMContext):
    await state.update_data(region=message.text)
    await message.answer("Укажите ориентир (например: Ойбек, Мирабадский район):")
    await state.set_state(AnnouncementForm.orientir)


@router.message(AnnouncementForm.orientir)
async def process_orientir(message: Message, state: FSMContext):
    await state.update_data(orientir=message.text)
    await message.answer(
        "Сколько комнат?",
        reply_markup=rooms_buttons()
    )
    await state.set_state(AnnouncementForm.rooms)


@router.callback_query(AnnouncementForm.rooms)
async def process_rooms(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "custom_rooms":
        await callback.message.edit_text("Введите количество комнат:")
    else:
        await state.update_data(rooms=callback.data)
        await callback.message.edit_text("Сколько всего этажей в здании?")
        await state.set_state(AnnouncementForm.total_floors)
    await callback.answer()


@router.message(AnnouncementForm.rooms)
async def process_custom_rooms(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(rooms=message.text)
        await message.answer("Сколько всего этажей в здании?")
        await state.set_state(AnnouncementForm.total_floors)
    else:
        await message.answer("Пожалуйста, введите число")


@router.message(AnnouncementForm.total_floors)
async def process_total_floors(message: Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 50:
        await state.update_data(total_floors=message.text)
        data = await state.get_data()
        await message.answer(
            f"На каком этаже находится недвижимость? (1-{data['total_floors']})",
            reply_markup=floor_buttons(data['total_floors'])
        )
        await state.set_state(AnnouncementForm.floor)
    else:
        await message.answer("Пожалуйста, введите корректное число этажей (1-50)")


@router.callback_query(AnnouncementForm.floor)
async def process_floor(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "custom_floor":
        await callback.message.edit_text("Введите номер этажа:")
    else:
        await state.update_data(floor=callback.data)
        await callback.message.edit_text("Какое состояние недвижимости?", reply_markup=condition_buttons())
        await state.set_state(AnnouncementForm.condition)
    await callback.answer()


@router.message(AnnouncementForm.floor)
async def process_custom_floor(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(floor=message.text)
        await message.answer("Какое состояние недвижимости?", reply_markup=condition_buttons())
        await state.set_state(AnnouncementForm.condition)
    else:
        await message.answer("Пожалуйста, введите число")


@router.callback_query(AnnouncementForm.condition)
async def process_condition(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "custom_condition":
        await callback.message.edit_text("Введите состояние недвижимости:")
    else:
        await state.update_data(condition=callback.data)
        data = await state.get_data()
        await callback.message.edit_text(
            "Какие дополнительные особенности есть?\n(Выберите все подходящие варианты)",
            reply_markup=get_feature_buttons(data.get('additional_features', []))
        )
        await state.set_state(AnnouncementForm.additional_features)
    await callback.answer()


@router.message(AnnouncementForm.condition)
async def process_custom_condition(message: Message, state: FSMContext):
    await state.update_data(condition=message.text)
    data = await state.get_data()
    await message.answer(
        "Какие дополнительные особенности есть?\n(Выберите все подходящие варианты)",
        reply_markup=get_feature_buttons(data.get('additional_features', []))
    )
    await state.set_state(AnnouncementForm.additional_features)


@router.callback_query(AnnouncementForm.additional_features)
async def process_features(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get('additional_features', [])
    custom = data.get('custom_features', [])

    if callback.data == "done":
        if not selected and not custom:
            await callback.answer("Выберите хотя бы одну особенность", show_alert=True)
            return

        await callback.message.edit_text("Укажите цену (например: 345.000 y.e./торг на месте):")
        await state.set_state(AnnouncementForm.price)

    elif callback.data == "add_custom":
        await callback.message.edit_text("Введите свою особенность:")
        await state.set_state(AnnouncementForm.custom_feature_input)

    elif callback.data.startswith("custom_"):
        # Toggle custom feature
        feature = callback.data[7:]  # Remove "custom_" prefix
        if feature in custom:
            custom.remove(feature)
        else:
            custom.append(feature)
        await state.update_data(custom_features=custom)
        await show_feature_selection(callback.message, selected, custom)

    else:
        # Toggle essential feature
        if callback.data in selected:
            selected.remove(callback.data)
        else:
            selected.append(callback.data)
        await state.update_data(additional_features=selected)
        await show_feature_selection(callback.message, selected, custom)

    await callback.answer()


@router.message(AnnouncementForm.custom_feature_input)
async def process_custom_feature(message: Message, state: FSMContext):
    data = await state.get_data()
    custom = data.get('custom_features', [])

    if message.text.strip():
        custom.append(message.text.strip())
        await state.update_data(custom_features=custom)

    # Return to feature selection
    data = await state.get_data()
    await message.answer(
        "Какие дополнительные особенности есть?",
        reply_markup=get_feature_buttons(
            data.get('additional_features', []),
            data.get('custom_features', [])
        )
    )
    await state.set_state(AnnouncementForm.additional_features)


async def show_feature_selection(message: Message, selected: list, custom: list):
    # Group features into categories
    features_by_category = {
        "Строительство и материалы": [
            ("electricity", "Электрика есть"),
            ("plastered_walls", "Стены заштукатурены"),
            ("poured_floor", "Пол залит"),
            ("brick_walls", "Кирпичные стены"),
            ("monolithic", "Монолитное строительство"),
            ("panel", "Панельный дом"),
            ("new_building", "Новостройка"),
            ("secondary", "Вторичное жилье"),
        ],
        "Помещения": [
            ("wardrobe", "Гардеробная"),
            ("storage", "Кладовая"),
            ("balcony", "Балкон"),
            ("loggia", "Лоджия"),
            ("terrace", "Терраса"),
            ("veranda", "Веранда"),
            ("attic", "Мансарда"),
            ("basement", "Подвал"),
        ],
        "Кухня": [
            ("kitchen_furniture", "Кухонная мебель"),
            ("kitchen_appliances", "Встроенная техника"),
            ("bar_counter", "Барная стойка"),
            ("kitchen_island", "Островная кухня"),
        ],
        "Санузел": [
            ("jacuzzi", "Джакузи"),
            ("sauna", "Сауна"),
            ("steam_room", "Парная"),
            ("separate_toilet", "Раздельный санузел"),
            ("bathroom_renovation", "Санузел с ремонтом"),
        ],
        "Технические особенности": [
            ("heating", "Отопление"),
            ("gas", "Газ"),
            ("central_heating", "Центральное отопление"),
            ("individual_heating", "Индивидуальное отопление"),
            ("water_supply", "Водоснабжение"),
            ("sewage", "Канализация"),
            ("ventilation", "Вентиляция"),
            ("fireplace", "Камин"),
            ("smart_home", "Умный дом"),
        ],
        "Безопасность": [
            ("security", "Охрана"),
            ("concierge", "Консьерж"),
            ("cctv", "Видеонаблюдение"),
            ("alarm", "Сигнализация"),
            ("intercom", "Домофон"),
        ],
        "Территория": [
            ("pool", "Бассейн"),
            ("parking", "Парковка"),
            ("underground_parking", "Подземная парковка"),
            ("garage", "Гараж"),
            ("garden", "Сад"),
            ("playground", "Детская площадка"),
            ("barbecue", "Зона барбекю"),
            ("fountain", "Фонтан"),
        ],
        "Инфраструктура": [
            ("elevator", "Лифт"),
            ("freight_elevator", "Грузовой лифт"),
            ("ramp", "Пандус"),
            ("gym", "Тренажерный зал"),
            ("spa", "СПА-зона"),
            ("laundry", "Прачечная"),
            ("conference_room", "Конференц-зал"),
        ],
        "Дополнительные удобства": [
            ("air_conditioning", "Кондиционер"),
            ("wifi", "Wi-Fi"),
            ("cable_tv", "Кабельное ТВ"),
            ("soundproofing", "Шумоизоляция"),
            ("view", "Вид из окна"),
            ("panoramic_windows", "Панорамные окна"),
            ("fire_exit", "Пожарный выход"),
        ],
        "Специальные особенности": [
            ("designer_renovation", "Дизайнерский ремонт"),
            ("euro_renovation", "Евроремонт"),
            ("fresh_renovation", "Свежий ремонт"),
            ("historical", "Историческая ценность"),
            ("waterfront", "Водоем рядом"),
            ("green_zone", "Зеленая зона"),
            ("quiet_courtyard", "Тихий двор"),
        ]
    }

    # Create inline keyboard with categorized features
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    # Add categorized features
    for category, features in features_by_category.items():
        row_buttons = []
        for feature_id, feature_name in features:
            emoji = "✅" if feature_id in selected else "⬜"
            row_buttons.append(InlineKeyboardButton(
                text=f"{emoji} {feature_name}",
                callback_data=feature_id
            ))
            if len(row_buttons) == 2:  # 2 buttons per row
                keyboard.inline_keyboard.append(row_buttons)
                row_buttons = []
        if row_buttons:  # Add remaining buttons if any
            keyboard.inline_keyboard.append(row_buttons)

    # Add custom features if any
    if custom:
        keyboard.inline_keyboard.append([InlineKeyboardButton(
            text="══════ Ваши особенности ══════",
            callback_data="ignore"
        )])
        row_buttons = []
        for feature in custom:
            emoji = "✅" if feature in custom else "⬜"
            row_buttons.append(InlineKeyboardButton(
                text=f"{emoji} {feature}",
                callback_data=f"custom_{feature}"
            ))
            if len(row_buttons) == 2:
                keyboard.inline_keyboard.append(row_buttons)
                row_buttons = []
        if row_buttons:
            keyboard.inline_keyboard.append(row_buttons)

    # Add action buttons
    keyboard.inline_keyboard.extend([
        [InlineKeyboardButton(text="➕ Добавить свою особенность", callback_data="add_custom")],
        [InlineKeyboardButton(text="✅ Готово", callback_data="done")]
    ])

    await message.edit_text(
        "Выберите особенности недвижимости:",
        reply_markup=keyboard
    )


@router.message(AnnouncementForm.price)
async def process_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()

    # Generate announcement with fixed contact info
    property_type = {
        "apartment": "квартира",
        "house": "дом",
        "commercial": "коммерческая недвижимость",
        "land": "земельный участок"
    }.get(data['property_type'], "недвижимость")

    rooms = data['rooms']
    room_text = f"{rooms}-комнатная" if rooms != "1" else "1-комнатная"

    if data.get('jkh_name'):
        jkh_map = {
            "nrg_oybek": "ЖК NRG Oybek",
            "kamron_palace": "ЖК Kamron Palace",
            "central_park": "ЖК Central Park",
            "other_jkh": "ЖК"
        }
        location = jkh_map.get(data['jkh_name'], "ЖК")
    else:
        region_map = {
            "chilanzar": "Чиланзарский район",
            "yunusabad": "Юнусабадский район",
            "mirabad": "Мирабадский район",
            "shaykhontokhur": "Шайхантахурский район",
            "other_region": "другой район"
        }
        location = region_map.get(data.get('region', ''), "")

    condition_map = {
        "euro_lux": "Евролюкс",
        "box": "Коробка",
        "luxury": "Luxury интерьер",
        "euro_repair": "Евро ремонт",
        "rough": "Черновая отделка",
        "pre_finish": "Предчистовая отделка"
    }
    condition = condition_map.get(data['condition'], "")

    feature_map = {
        # Construction and materials
        "electricity": "Электрика есть",
        "plastered_walls": "Стены заштукатурены",
        "poured_floor": "Пол залит",
        "brick_walls": "Кирпичные стены",
        "monolithic": "Монолитное строительство",
        "panel": "Панельный дом",
        "new_building": "Новостройка",
        "secondary": "Вторичное жилье",

        # Rooms and spaces
        "wardrobe": "Гардеробная",
        "storage": "Кладовая",
        "balcony": "Балкон",
        "loggia": "Лоджия",
        "terrace": "Терраса",
        "veranda": "Веранда",
        "attic": "Мансарда",
        "basement": "Подвал",

        # Kitchen features
        "kitchen_furniture": "Кухонная мебель",
        "kitchen_appliances": "Встроенная техника",
        "bar_counter": "Барная стойка",
        "kitchen_island": "Островная кухня",

        # Bathroom features
        "jacuzzi": "Джакузи",
        "sauna": "Сауна",
        "steam_room": "Парная",
        "separate_toilet": "Раздельный санузел",
        "bathroom_renovation": "Санузел с ремонтом",

        # Technical features
        "heating": "Отопление",
        "gas": "Газ",
        "central_heating": "Центральное отопление",
        "individual_heating": "Индивидуальное отопление",
        "water_supply": "Водоснабжение",
        "sewage": "Канализация",
        "ventilation": "Вентиляция",
        "fireplace": "Камин",
        "smart_home": "Умный дом",

        # Security
        "security": "Охрана",
        "concierge": "Консьерж",
        "cctv": "Видеонаблюдение",
        "alarm": "Сигнализация",
        "intercom": "Домофон",

        # Outdoor amenities
        "pool": "Бассейн",
        "parking": "Парковка",
        "underground_parking": "Подземная парковка",
        "garage": "Гараж",
        "garden": "Сад",
        "playground": "Детская площадка",
        "barbecue": "Зона барбекю",
        "fountain": "Фонтан",

        # Infrastructure
        "elevator": "Лифт",
        "freight_elevator": "Грузовой лифт",
        "ramp": "Пандус",
        "gym": "Тренажерный зал",
        "spa": "СПА-зона",
        "laundry": "Прачечная",
        "conference_room": "Конференц-зал",

        # Additional comforts
        "air_conditioning": "Кондиционер",
        "wifi": "Wi-Fi",
        "cable_tv": "Кабельное ТВ",
        "soundproofing": "Шумоизоляция",
        "view": "Вид из окна",
        "panoramic_windows": "Панорамные окна",
        "fire_exit": "Пожарный выход",

        # Special features
        "designer_renovation": "Дизайнерский ремонт",
        "euro_renovation": "Евроремонт",
        "fresh_renovation": "Свежий ремонт",
        "historical": "Историческая ценность",
        "waterfront": "Водоем рядом",
        "green_zone": "Зеленая зона",
        "quiet_courtyard": "Тихий двор"
    }
    features = "\n".join([feature_map.get(f, "") for f in data['additional_features']])

    announcement = (
        f"<b><i>Продаётся {room_text} {property_type} в {location}</i></b>\n\n"
        f"Ориентир: {data['orientir']}\n\n"
        f"Комнат: {rooms}\n"
        f"Этаж: {data['floor']}\n"
        f"Этажность: {data['total_floors']}\n"
        f"Общая площадь: (укажите площадь) м²\n\n"
        f"Состояние: {condition}\n"
        f"{features}\n\n"
        f"Цена: {data['price']}\n\n"
        f"+998909946644 Улугбек\n"
        f"t.me/akhulugbek"
    )

    await message.answer(announcement, parse_mode="HTML")
    await state.clear()
