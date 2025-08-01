import http.client
import json
import os

headers = {
    "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY", ""),
    "Content-Type": "application/json",
}
# 支持的语言选项
LANGUAGES = {
    "自动检测": "auto",
    "英语": "English",
    "简体中文": "Chinese",
    "繁体中文": "Traditional Chinese",
    "俄语": "Russian",
    "日语": "Japanese",
    "韩语": "Korean",
    "西班牙语": "Spanish",
    "法语": "French",
    "葡萄牙语": "Portuguese",
    "德语": "German",
    "意大利语": "Italian",
    "泰语": "Thai",
    "越南语": "Vietnamese",
    "印度尼西亚语": "Indonesian",
    "马来语": "Malay",
    "阿拉伯语": "Arabic",
    "印地语": "Hindi",
    "希伯来语": "Hebrew",
    "缅甸语": "Burmese",
    "泰米尔语": "Tamil",
    "乌尔都语": "Urdu",
    "孟加拉语": "Bengali",
    "波兰语": "Polish",
    "荷兰语": "Dutch",
    "罗马尼亚语": "Romanian",
    "土耳其语": "Turkish",
    "高棉语": "Khmer",
    "老挝语": "Lao",
    "粤语": "Cantonese",
    "捷克语": "Czech",
    "希腊语": "Greek",
    "瑞典语": "Swedish",
    "匈牙利语": "Hungarian",
    "丹麦语": "Danish",
    "芬兰语": "Finnish",
    "乌克兰语": "Ukrainian",
    "保加利亚语": "Bulgarian",
    "塞尔维亚语": "Serbian",
    "泰卢固语": "Telugu",
    "南非荷兰语": "Afrikaans",
    "亚美尼亚语": "Armenian",
    "阿萨姆语": "Assamese",
    "阿斯图里亚斯语": "Asturian",
    "巴斯克语": "Basque",
    "白俄罗斯语": "Belarusian",
    "波斯尼亚语": "Bosnian",
    "加泰罗尼亚语": "Catalan",
    "宿务语": "Cebuano",
    "克罗地亚语": "Croatian",
    "埃及阿拉伯语": "Egyptian Arabic",
    "爱沙尼亚语": "Estonian",
    "加利西亚语": "Galician",
    "格鲁吉亚语": "Georgian",
    "古吉拉特语": "Gujarati",
    "冰岛语": "Icelandic",
    "爪哇语": "Javanese",
    "卡纳达语": "Kannada",
    "哈萨克语": "Kazakh",
    "拉脱维亚语": "Latvian",
    "立陶宛语": "Lithuanian",
    "卢森堡语": "Luxembourgish",
    "马其顿语": "Macedonian",
    "马加希语": "Maithili",
    "马耳他语": "Maltese",
    "马拉地语": "Marathi",
    "美索不达米亚阿拉伯语": "Mesopotamian Arabic",
    "摩洛哥阿拉伯语": "Moroccan Arabic",
    "内志阿拉伯语": "Najdi Arabic",
    "尼泊尔语": "Nepali",
    "北阿塞拜疆语": "North Azerbaijani",
    "北黎凡特阿拉伯语": "North Levantine Arabic",
    "北乌兹别克语": "Northern Uzbek",
    "书面语挪威语": "Norwegian Bokmål",
    "新挪威语": "Norwegian Nynorsk",
    "奥克语": "Occitan",
    "奥里亚语": "Odia",
    "邦阿西楠语": "Pangasinan",
    "西西里语": "Sicilian",
    "信德语": "Sindhi",
    "僧伽罗语": "Sinhala",
    "斯洛伐克语": "Slovak",
    "斯洛文尼亚语": "Slovenian",
    "南黎凡特阿拉伯语": "South Levantine Arabic",
    "斯瓦希里语": "Swahili",
    "他加禄语": "Tagalog",
    "塔伊兹-亚丁阿拉伯语": "Ta’izzi-Adeni Arabic",
    "托斯克阿尔巴尼亚语": "Tosk Albanian",
    "突尼斯阿拉伯语": "Tunisian Arabic",
    "威尼斯语": "Venetian",
    "瓦莱语": "Waray",
    "威尔士语": "Welsh",
    "西波斯语": "Western Persian",
}


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    调用阿里云百炼的翻译模型进行翻译
    """
    if not text.strip():
        return "请输入要翻译的文本"

    try:
        # 调用模型
        conn = http.client.HTTPSConnection("dashscope.aliyuncs.com")
        json_data = {
            "model": "qwen-mt-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": text,
                },
            ],
            "translation_options": {
                "source_lang": LANGUAGES.get(source_lang, "auto"),
                "target_lang": LANGUAGES.get(target_lang, "English"),
            },
        }
        conn.request(
            "POST",
            "/compatible-mode/v1/chat/completions",
            json.dumps(json_data),
            headers,
        )
        response = conn.getresponse()
        resp_str = response.read().decode("utf-8")
        resp_json = json.loads(resp_str)
        return resp_json["choices"][0]["message"]["content"]
    except Exception as e:
        return f"翻译出错: {str(e)}"


def main():
    target_lang = "英语"
    source_lang = "简体中文"
    prompt_str = "汉译英> "
    while True:
        try:
            text: str = input(prompt_str)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            if text.startswith("\\e"):
                target_lang = "简体中文"
                source_lang = "英语"
                print("Translate English to Chinese")
                prompt_str = "En2Ch> "
            elif text.startswith("\\c"):
                target_lang = "英语"
                source_lang = "简体中文"
                prompt_str = "汉译英> "
                print("翻译成英文")
            else:
                print(
                    translate_text(
                        text, target_lang=target_lang, source_lang=source_lang
                    )
                )
    print("GoodBye!")


if __name__ == "__main__":
    main()
