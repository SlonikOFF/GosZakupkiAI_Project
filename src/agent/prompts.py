from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

DECIDE_SEARCH_PROMPT_TEMPLATE = """Оцени следующий запрос пользователя по госзакупкам (44-ФЗ, 223-ФЗ).
Нужно ли для точного, актуального и полного ответа искать информацию на внешних доверенных ресурсах (законы, статьи, практика, конкретные детали)?
Ответь ТОЛЬКО ОДНИМ СЛОВОМ: YES или NO.

Запрос пользователя:
{user_query}
"""
DECIDE_SEARCH_PROMPT = PromptTemplate.from_template(DECIDE_SEARCH_PROMPT_TEMPLATE)

GENERATE_SEARCH_QUERY_PROMPT_TEMPLATE = """Проанализируй запрос пользователя по госзакупкам.
Твоя задача - сгенерировать ОДИН, наиболее эффективный и точный поисковый запрос на русском языке для поиска релевантной информации на доверенных сайтах (zakupki.gov.ru, consultant.ru, garant.ru и т.д.).

ИНСТРУКЦИИ ПО ГЕНЕРАЦИИ ЗАПРОСА:
1.  Определи ключевые термины и понятия в запросе пользователя.
2.  **Критически важно:** Попытайся понять, относится ли запрос к 44-ФЗ (государственные и муниципальные закупки) или к 223-ФЗ (закупки отдельных видов юридических лиц / госкомпаний).
3.  **Обязательно добавь "44-ФЗ" или "223-ФЗ" к поисковому запросу**, если это явно указано или уверенно предполагается из контекста (например, "госзаказ", "бюджетные учреждения" -> 44-ФЗ; "закупки госкорпорации", "положение о закупке" -> 223-ФЗ). Если закон не ясен, НЕ добавляй номер закона, а сделай запрос более общим, но точным по терминам.
4.  Сфокусируй запрос на конкретном аспекте, интересующем пользователя (например, "порядок проведения", "требования к участникам", "ответственность", "сроки", "обеспечение контракта").
5.  Запрос должен быть лаконичным, но информативным.

Выведи ТОЛЬКО САМ ПОИСКОВЫЙ ЗАПРОС, без каких-либо пояснений, кавычек или префиксов.

Примеры:
Запрос пользователя: "Как подать заявку на участие в электронном аукционе для СМП?"
Результат: "подача заявки электронный аукцион СМП 44-ФЗ"

Запрос пользователя: "Нужно ли публиковать план закупок по 223-ФЗ на zakupki.gov?"
Результат: "публикация плана закупок 223-ФЗ zakupki.gov"

Запрос пользователя: "Что такое обеспечение исполнения контракта?"
Результат: "обеспечение исполнения контракта 44-ФЗ" (44-ФЗ более вероятен для общего вопроса)

Запрос пользователя: "Какая ответственность за неразмещение отчета в ЕИС?"
Результат: "ответственность неразмещение отчета ЕИС 223-ФЗ" (если контекст указывает на 223-ФЗ) или "ответственность неразмещение отчета ЕИС 44-ФЗ" (если контекст указывает на 44-ФЗ)

Запрос пользователя: "Как участвовать в аукционах?" (Общий)
Результат: "участие в электронных аукционах порядок 44-ФЗ" (44-ФЗ более общий)

Начинаем!

Запрос пользователя:
{user_query}
"""
GENERATE_SEARCH_QUERY_PROMPT = PromptTemplate.from_template(GENERATE_SEARCH_QUERY_PROMPT_TEMPLATE)


SYNTHESIZE_ANSWER_PROMPT_TEMPLATE = """Ты — эксперт-ассистент по госзакупкам в Российской Федерации (44-ФЗ и 223-ФЗ).
Твоя задача — дать ПОЛНЫЙ, ТОЧНЫЙ и СТРУКТУРИРОВАННЫЙ ответ на запрос пользователя, основываясь **ИСКЛЮЧИТЕЛЬНО** на предоставленной ниже информации.

ИСХОДНЫЕ ДАННЫЕ:
1.  **Запрос Пользователя:** {user_query}
2.  **Результаты Поиска на Доверенных Ресурсах:**
    {search_results_context}

ИНСТРУКЦИИ:
*   Внимательно проанализируй запрос пользователя и результаты поиска.
*   Синтезируй ответ, который наилучшим образом отвечает на запрос пользователя, используя информацию из результатов поиска.
*   **ВАЖНО:** Если ты используешь информацию из 'Результаты Поиска', которая начинается с `... (источник: [URL], ...)...`, **обязательно указывай URL источника** после соответствующего утверждения в твоем ответе, например: "[утверждение из текста] (Источник: [URL])". Старайся группировать информацию из одного источника, чтобы не повторять ссылку слишком часто.
*   Если результаты поиска содержат сообщение об ошибке (например, "Ошибка поиска", "Не удалось загрузить", "Не удалось извлечь информацию"), сообщи об этом пользователю и отвечай на основе своих общих знаний, но СДЕЛАЙ ЯВНУЮ ПОМЕТКУ, что информация может быть неполной или неактуальной из-за невозможности проверить ее по внешним источникам.
*   Если поиск не проводился (в результатах указано "Поиск не проводился..."), отвечай на основе своих знаний.
*   Ответ должен быть на русском языке, вежливым, профессиональным и хорошо структурированным (используй списки, параграфы).
*   НЕ добавляй в ответ никакой информации, которой нет в исходных данных (запросе и результатах поиска), если только ты не указываешь, что это твои общие знания из-за проблем с поиском.
*   НЕ упоминай сам процесс поиска или анализа, если только не нужно сообщить об ошибке поиска. Просто дай ответ по существу.

ФИНАЛЬНЫЙ ОТВЕТ:
"""
SYNTHESIZE_ANSWER_PROMPT = PromptTemplate.from_template(SYNTHESIZE_ANSWER_PROMPT_TEMPLATE)