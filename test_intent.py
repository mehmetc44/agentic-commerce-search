import sys
import os
import json
import pprint

# Python modül arama yoluna 'src' klasörünü ekliyoruz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from chatbot.agents.intent_analyser import IntentAnalyserAgent

def run_test():
    print("🤖 IntentAnalyserAgent yükleniyor...")
    try:
        agent = IntentAnalyserAgent(temperature=0.0)
    except Exception as e:
        print(f"❌ Ajan başlatılamadı (Ollama çalışıyor mu?): {e}")
        return

    # Test etmek istediğiniz sorguyu buraya yazabilirsiniz:
    test_query = "waterproof winter boots for baby girl in black, budget under 1000 TL"
    
    print(f"\n🔍 Test sorgusu gönderiliyor: '{test_query}'")
    print("LLM yanıtı bekleniyor...")
    
    try:
        result = agent.analyze(test_query)
        print("\n✅ Analiz başarıyla tamamlandı! Sonuç:\n")
        pprint.pprint(result)
    except Exception as e:
        print(f"❌ Analiz sırasında hata oluştu: {e}")

if __name__ == "__main__":
    run_test()
