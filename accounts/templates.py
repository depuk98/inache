# coding:utf-8
import csv


# Opening JSON file and loading the data
# into the variable data
# with open('data.json') as json_file:
data = [
    {
        "Title": "General case/ English",
        "TempId": "1707164006816885341",
        "body": "Thank you very much for informing us about this issue. ${aboutDetails}. We will resolve this problem as soon as possible. Thank you for using Inache Service.",
    },
    {
        "Title": "Acknowledgement of Complaint/ English",
        "TempId": "1707164015688677345",
        "body": "Your case has been recieved at ${aboutDetails} department. We will solve it as soon as possible. In case we need any further details, you will be contacted soon. Thank you for using Inache Service.",
    },
    {
        "Title": "Closing the case/ English",
        "TempId": "1707164006751946646",
        "body": "Your issue about ${aboutDetails} with case number ${aboutDetails} has been closed. Thank you for using Ianche Service. Please Do Not respond to this message.",
    },
    {
        "Title": "Reporting for resolution/ English",
        "TempId": "1707163767033820913",
        "body": "You are required to visit ${aboutDetails} department to proceed further in resolution of your case no. ${aboutDetails} within ${aboutDetails} days. Please DO NOT respond to this message. Thank you for using INACHE Service.",
    },
    {
        "Title": "Special case/ English",
        "TempId": "1707164006788611821",
        "body": "Thank you very much for informing us about this serious issue through Inache. We will resolve this problem as soon as possible. Thank you for using Inache Service.",
    },
    {
        "Title": "General case/ Hindi",
        "TempId": "1707164006836695885",
        "body": "इस मुद्दे के बारे में हमें सूचित करने के लिए आपका बहुत-बहुत धन्यवाद। ${aboutDetails}। हम जल्द से जल्द इस समस्या का समाधान करेंगे। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद।",
    },
    {
        "Title": "Acknowledgement of Complaint/ Hindi",
        "TempId": "1707164015694134992",
        "body": "आपका केस ${aboutDetails} विभाग को प्राप्त हो गया है। हम इसका जल्द से जल्द समाधान किया जाएगा। यदि हमें और किसी जानकारी की आवश्यकता होती है तो आपसे शीघ्र ही संपर्क किया जाएगा। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद।",
    },
    {
        "Title": "Closing the case/ Hindi",
        "TempId": "1707164006757168568",
        "body": "आपके ${aboutDetails} के मुद्दे से जुड़ा केस नंबर ${aboutDetails} बंद कर दिया गया है।ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। कृपया इस संदेश का जवाब ना दें।",
    },
    {
        "Title": "Reporting for resolution/ Hindi",
        "TempId": "1707163767217628717",
        "body": "आपके केस नंबर ${aboutDetails} के समाधान में आगे बढ़ने के लिए आपको ${aboutDetails} दिनों के भीतर ${aboutDetails} विभाग में जाना पड़ेगा। कृपया इस संदेश का उत्तर न दें। ईनाचे सेवा का उपयोग करने के लिए आपका धन्यवाद।",
    },
    {
        "Title": "Special case/ Hindi",
        "TempId": "1707164006793701646",
        "body": "ईनाचे के माध्यम से हमें इस गंभीर मुद्दे के बारे में सूचित करने के लिए आपका बहुत-बहुत धन्यवाद। हम इस समस्या का जल्द से जल्द समाधान करेंगे। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद।",
    },
    {
        "Title": "General case/ Punjabi",
        "TempId": "1707164006844113653",
        "body": "ਇਸ ਮੁੱਦੇ ਬਾਰੇ ਸਾਨੂੰ ਸੂਚਿਤ ਕਰਨ ਲਈ ਤੁਹਾਡਾ ਬਹੁਤ-ਬਹੁਤ ਧੰਨਵਾਦ। ${aboutDetails}। ਅਸੀਂ ਇਸ ਸਮੱਸਿਆ ਨੂੰ ਜਲਦੀ ਤੋਂ ਜਲਦੀ ਹੱਲ ਕਰ ਕਰਾਂਗੇ। ਇਨਾਚੇ ਸੇਵਾ ਦੀ ਵਰਤੋਂ ਕਰਨ ਲਈ ਤੁਹਾਡਾ ਧੰਨਵਾਦ।",
    },
    {
        "Title": "Acknowledgement of Complaint/ Punjabi",
        "TempId": "1707164015699564466",
        "body": "ਤੁਹਾਡਾ ਕੇਸ ${aboutDetails} ਵਿਭਾਗ ਨੂੰ ਪ੍ਰਾਪਤ ਹੋ ਗਿਆ ਹੈ। ਅਸੀਂ ਜਿੰਨੀ ਜਲਦੀ ਹੋ ਸਕੇ ਇਸ ਸਮੱਸਿਆ ਨੂੰ ਹੱਲ ਕਰਾਂਗੇ। ਜੇਕਰ ਸਾਨੂੰ ਕਿਸੇ ਹੋਰ ਵੇਰਵਿਆਂ ਦੀ ਲੋੜ ਪਈ ਤਾਂ ਤੁਹਾਡੇ ਨਾਲ ਜਲਦੀ ਹੀ ਸੰਪਰਕ ਕਰਾਂਗੇ। ਇਨਾਚੇ ਸੇਵਾ ਦੀ ਵਰਤੋਂ ਕਰਨ ਲਈ ਤੁਹਾਡਾ ਧੰਨਵਾਦ।",
    },
    {
        "Title": "Closing the case/ Punjabi",
        "TempId": "1707164006763040811",
        "body": "ਤੁਹਾਡੇ ${aboutDetails} ਸਮੱਸਿਆ ਨਾਲ ਸਬੰਧਿਤ ਕੇਸ ਨੰਬਰ ${aboutDetails} ਨੂੰ ਬੰਦ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ। ਇਨਾਚੇ ਸੇਵਾ ਦੀ ਵਰਤੋਂ ਕਰਨ ਲਈ ਤੁਹਾਡਾ ਧੰਨਵਾਦ। ਕਿਰਪਾ ਕਰਕੇ ਇਸ ਸੁਨੇਹੇ ਦਾ ਜਵਾਬ ਨਾ ਦਿਓ।",
    },
    {
        "Title": "Reporting for resolution/ Punjabi",
        "TempId": "1707163767224137015",
        "body": "ਤੁਹਾਨੂੰ ਆਪਣੇ ਕੇਸ ਨੰਬਰ ${aboutDetails} ਦੇ ਹੱਲ ਵਿੱਚ ਅੱਗੇ ਵਧਣ ਲਈ ${aboutDetails} ਦਿਨਾਂ ਦੇ ਅੰਦਰ ${aboutDetails} ਵਿਭਾਗ ਜਾਣਾ ਵਿੱਚ ਪਵੇਗਾ। ਕਿਰਪਾ ਕਰਕੇ ਇਸ ਸੰਦੇਸ਼ ਦਾ ਜਵਾਬ ਨਾ ਦਿਓ। ਇਨਾਚੇ ਸੇਵਾ ਦੀ ਵਰਤੋਂ ਕਰਨ ਲਈ ਤੁਹਾਡਾ ਧੰਨਵਾਦ।",
    },
    {
        "Title": "Special case/ Punjabi",
        "TempId": "1707164006799070640",
        "body": "ਇਨਾਚੇ ਦੁਆਰਾ ਸਾਨੂੰ ਇਸ ਗੰਭੀਰ ਮੁੱਦੇ ਬਾਰੇ ਸੂਚਿਤ ਕਰਨ ਲਈ ਤੁਹਾਡਾ ਬਹੁਤ ਬਹੁਤ ਧੰਨਵਾਦ। ਅਸੀਂ ਇਸ ਸਮੱਸਿਆ ਨੂੰ ਜਲਦੀ ਤੋਂ ਜਲਦੀ ਹੱਲ ਕਰਾਂਗੇ। ਇਨਾਚੇ ਸੇਵਾ ਦੀ ਵਰਤੋਂ ਕਰਨ ਲਈ ਤੁਹਾਡਾ ਧੰਨਵਾਦ।",
    },
    {
        "Title": "General case/ Kannada",
        "TempId": "1707164622333122953",
        "body": "ಈ {#var#} ಸಮಸ್ಯೆಯ ಬಗ್ಗೆ ನಮಗೆ ತಿಳಿಸಿದ್ದಕ್ಕಾಗಿ ತುಂಬಾ ಧನ್ಯವಾದಗಳು. ನಾವು ಈ ಸಮಸ್ಯೆಯನ್ನು ಸಾಧ್ಯವಾದಷ್ಟು ಬೇಗ ಪರಿಹರಿಸುತ್ತೇವೆ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Resolution/ English",
        "TempId": "1707166928362829827",
        "body": "Your case about ${aboutDetails} has been resolved. Kindly say "
        "YES, I am satisfied"
        ", if you are satisfied or "
        "NO, I am not satisfied"
        " if you are not satisfied with the resolution. Kindly Do Not respond to this message. Please send your voice-recorded reply to ${inacheNo} number. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Case registration acknowledgement/ English",
        "TempId": "1707164621568880677",
        "body": "Thank you for using Inache Service. Your Case No is {#var#}. Please DO NOT respond to this message. Send your reply to Inache number {#var#} . Shahi Management",
    },
    {
        "Title": "POSH case 1/ English",
        "TempId": "1707164621448129554",
        "body": "hank you for informing us about this issue. We are here to help you. Your identity will not be revealed anywhere. Kindly meet the ICC Rep. {#var#} and file a written complaint for redressal. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "General Reminder for using Inache/ English",
        "TempId": "1707164621585857567",
        "body": "Please share your suggestions, queries, and problems on Inache number {#var#}. Shahi Management",
    },
    {
        "Title": "General Reminder for using Inache/ Hindi",
        "TempId": "1707164622350747323",
        "body": "कृपया अपने सुझावों, प्रश्नों और समस्याओं को Inache नंबर {#var#} पर साझा करें। Shahi प्रबंधन",
    },
    {
        "Title": "Employee vaccination/ Hindi",
        "TempId": "1707164622359370972",
        "body": "{#var#} ने {#var#} अस्पताल के सहयोग से सभी कर्मचारियों के लिए निःशुल्क कोविड वैक्सीन {#var#} की व्यवस्था की है। इच्छुक लोगों से अनुरोध है कि वे अपना आधार कार्ड साथ लाएं और कारखाने में {#var#} से {#var#} के बीच टीकाकरण करवाएं। Shahi प्रबंधन",
    },
    {
        "Title": "Greetings 1/ Hindi",
        "TempId": "1707164622361714249",
        "body": "{#var#} के शुभ अवसर पर; हम Shahi परिवार की ओर से आपको बधाई देते है। हमें उम्मीद है कि यह अवसर आपके लिए सुख और समृद्धि लाएगा । अपने सुझाव या समस्या ईनाचे के नंबर {#var#} पर कॉल या मैसेज करके बताएं। Shahi प्रबंधन",
    },
    {
        "Title": "Greetings 1/ English",
        "TempId": "1707164621592008020",
        "body": "On the auspicious occasion of {#var#}; we, from the whole Shahi family, congratulate you. We hope this occasion will bring happiness and prosperity to you. Please share your suggestions or problems on Inache number {#var#}. Shahi Management.",
    },
    {
        "Title": "Greetings 2/ English",
        "TempId": "1707164621594565833",
        "body": "{#var#} best wishes for the day. Please share your suggestions or problems on Inache number {#var#}. Shahi Management.",
    },
    {
        "Title": "Emergency/Unprecedented event/ Hindi",
        "TempId": "1707164622367006931",
        "body": "{#var#} के मुद्दे के कारण,{#var#} विभाग/सुविधा {#var#} दिनों के लिए {#var#} से बंद रहेगा/ रहेगी। Shahi प्रबंधन",
    },
    {
        "Title": "Changes in timing of work and shifts/ Hindi",
        "TempId": "1707164622369551215",
        "body": "{#var#} से काम के साथ-साथ शिफ्ट के समय में भी बदलाव किया गया है। आपसे अनुरोध है कि पूरी जानकारी के लिए {#var#} देखें या मिले। Shahi प्रबंधन",
    },
    {
        "Title": "Promotions and increments/ Hindi",
        "TempId": "1707164622376380860",
        "body": "आप सभी को सूचित किया जाता है कि आने वाले {#var#} दिनों में HR विभाग द्वारा पदोन्नति और वेतन वृद्धि की घोषणा की जाएगी। इस संबंधी जानकारी का ध्यान रखे। कृपया इस संदेश का उत्तर न दें। ईनाचे सेवा का उपयोग करने के लिए आपका धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Health check up camp/ Hindi",
        "TempId": "1707164622379200940",
        "body": "{#var#} से {#var#} दिनों/तारीख़ तक स्वास्थ्य विभाग की ओर से स्वास्थ्य जांच कैंप का आयोजन किया जाएगा। आप सभी से अनुरोध है कि {#var#} से {#var#} समय के दरम्यान कैंप में पधारें। आगे की जानकारी के लिए अपने संबंधित रिपोर्टिंग अधिकारियों से मिलें । कृपया इस संदेश का उत्तर न दें। ईनाचे सेवा का उपयोग करने के लिए आपका धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Awareness sessions/ Hindi",
        "TempId": "1707164622381237227",
        "body": "{#var#} विभाग की ओर से {#var#} दिन/तारीख़ पर {#var#} से {#var#} समय के दरम्यान {#var#} के बारे में एक जागरूकता कैंप का आयोजन किया जा रहा है। आप सभी को इस कैंप में भाग लेने की आवश्यकता है। कैंप में आने के अपने समय की जानकारी के लिए अपने संबंधित रिपोर्टिंग अधिकारियों से मिलें। कृपया इस संदेश का उत्तर न दें। ईनाचे सेवा का उपयोग करने के लिए आपका धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Content of voice call-1/ Hindi",
        "TempId": "1707164622119730422",
        "body": "आपकी आवाज साफ नहीं है। कृपया ईनाचे नंबर {#var#} पर फिर से कॉल करें और बीप की ध्वनि के बाद अपनी समस्या स्पष्ट रूप से साझा करें। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Content of voice call-1/ Kannada",
        "TempId": "1707164622215439107",
        "body": "ನಿಮ್ಮ ಮಾತುಗಳು ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ. ದಯವಿಟ್ಟು ಇನಾಚೆ ಸಂಖ್ಯೆಗೆ {#var#} ಮತ್ತೊಮ್ಮೆ ಕರೆ ಮಾಡಿ ಮತ್ತು ಬೀಪ್ ಧ್ವನಿಯ ನಂತರ ನಿಮ್ಮ ಸಮಸ್ಯೆಗಳನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಹಂಚಿಕೊಳ್ಳಿ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Content of voice call-2/ Hindi",
        "TempId": "1707164622122028543",
        "body": "आपके वॉइस कॉल संदेश में आपकी समस्या के बारे में आवश्यक जानकारी का अभाव है। कृपया फिर से ईनाचे नंबर {#var#} पर कॉल करें और पूरी जानकारी दें।ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Content of voice call-2/ Kannada",
        "TempId": "1707164622223958201",
        "body": "ನಿಮ್ಮ ಕರೆ/ಸಂದೇಶದಲ್ಲಿ ನಿಮ್ಮ ಸಮಸ್ಯೆಯ ಕುರಿತು ಅಗತ್ಯವಿರುವ ಮಾಹಿತಿಯ ಕೊರತೆಯಿದೆ. ದಯವಿಟ್ಟು ಇನಾಚೆ ಸಂಖ್ಯೆಗೆ {#var#} ಮತ್ತೊಮ್ಮೆ ಕರೆ ಮಾಡಿ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Content of SMS/ Hindi",
        "TempId": "1707164622124919014",
        "body": "आपके SMS में आपकी समस्या से संबंधित उचित जानकारी का अभाव है। कृपया इसे पुनः भेजें और पूरी जानकारी दें। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Content of SMS/ Kannada",
        "TempId": "1707164622227595036",
        "body": "ನಿಮ್ಮ {#var#} ಸಂದೇಶ/ಕರೆಯಲ್ಲಿ ನಿಮ್ಮ ಸಮಸ್ಯೆಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಸರಿಯಾದ ಮಾಹಿತಿ ಇಲ್ಲ. ದಯವಿಟ್ಟು ಅದನ್ನು ಮರುಕಳುಹಿಸಿ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "POSH case 1/ Kannada",
        "TempId": "1707164622230368792",
        "body": "ಈ ಸಮಸ್ಯೆಯ ಬಗ್ಗೆ ನಮಗೆ ತಿಳಿಸಿದ್ದಕ್ಕಾಗಿ ತುಂಬಾ ಧನ್ಯವಾದಗಳು. ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ನಾವು ಇಲ್ಲಿದ್ದೇವೆ. ನಿಮ್ಮ ಗುರುತನ್ನು ಬಹಿರಂಗಪಡಿಸಲಾಗುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ICC ಪ್ರತಿನಿಧಿಯನ್ನು {#var#} ಭೇಟಿ ಮಾಡಿ ಮತ್ತು ದೂರು ಸಲ್ಲಿಸಿ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "POSH case 1/ Hindi",
        "TempId": "1707164622129437457",
        "body": "इस मुद्दे के बारे में हमें सूचित करने के लिए आपका धन्यवाद। हम आपकी सहायता करना चाहते हैं। आपकी पहचान गुप्त रखी जाएगी। कृपया ICC प्रतिनिधि {#var#} से मिलें और इस मामले के समाधान के लिए लिखित रूप में शिकायत दर्ज करें । ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "POSH case 2/ English",
        "TempId": "1707164621452148826",
        "body": "Thank you for informing us about this issue. This is a serious allegation. Kindly meet the ICC Rep. {#var#} and file a written complaint for redressal. You can also call on ICC Rep. phone number {#var#} and explain the problem in detail. We assure you that your identity will not be revealed anywhere and we will extent full support to you.Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "POSH case 2/ Hindi",
        "TempId": "1707164622132273599",
        "body": "इस मुद्दे के बारे में हमें सूचित करने के लिए आपका धन्यवाद। यह एक गंभीर आरोप है। कृपया ICC प्रतिनिधि {#var#} से मिलें और इस मामले के समाधान के लिए लिखित रूप में शिकायत दर्ज करें । आप ICC प्रतिनिधि के फ़ोन नंबर {#var#} पर भी कॉल कर सकते हैं और समस्या के बारे में विस्तार से बता सकते हैं। हम आपको विश्वास दिलाते हैं कि आपकी पहचान कहीं भी प्रकट नहीं की जाएगी और हम आपको पूर्ण समर्थन देंगे। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद Shahi प्रबंधन",
    },
    {
        "Title": "POSH case 2/ Kannada",
        "TempId": "1707164622233449731",
        "body": "ಈ ಸಮಸ್ಯೆಯ ಬಗ್ಗೆ ನಮಗೆ ತಿಳಿಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ಇದೊಂದು ಗಂಭೀರ ಆರೋಪ. ದಯವಿಟ್ಟು ICC ಪ್ರತಿನಿಧಿ{#var#} ಅವರನ್ನು ಭೇಟಿ ಮಾಡಿ. ಪರಿಹಾರಕ್ಕಾಗಿ ಲಿಖಿತ ದೂರು ಸಲ್ಲಿಸಿ. ನಿಮ್ಮ ಕಾರ್ಖಾನೆಯು ICC ಪ್ರತಿನಿಧಿ ಫೋನ್ ಸಂಖ್ಯೆಗೆ {#var#} ಕರೆ ಮಾಡಬಹುದು ಮತ್ತು ಸಮಸ್ಯೆಯನ್ನು ವಿವರವಾಗಿ ವಿವರಿಸಬಹುದು. ನಿಮ್ಮ ಗುರುತನ್ನು ಎಲ್ಲಿಯೂ ಬಹಿರಂಗಪಡಿಸಲಾಗುವುದಿಲ್ಲ ಎಂದು ನಾವು ನಿಮಗೆ ಭರವಸೆ ನೀಡುತ್ತೇವೆ ಮತ್ತು ಸಂಪೂರ್ಣ ಬೆಂಬಲವನ್ನು ನೀಡುತ್ತೇವೆ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "POSH case Follow-up/ English",
        "TempId": "1707164621518666050",
        "body": "We hope that you have shared the information by contacting the ICC representative {#var#}. We are there to support you. For any future problem or suggestion you can contact on Inache number {#var#}. Shahi Management",
    },
    {
        "Title": "POSH case Follow-up/ Hindi",
        "TempId": "1707164622134773930",
        "body": "हम आशा करतें है कि आपने ICC प्रतिनिधि {#var#}से संपर्क करके उनसे जानकारी साझा कर ली होगी। हम आपकी सहायता करना चाहते हैं। भविष्य में किसी भी समस्या या सुझाव के लिए आप ईनाचे नंबर {#var#} पर संपर्क कर सकती हैं। Shahi प्रबंधन",
    },
    {
        "Title": "POSH case Follow-up/ Kannada",
        "TempId": "1707164622245288531",
        "body": "ICC ಪ್ರತಿನಿಧಿ {#var#} ಅವರನ್ನು ಸಂಪರ್ಕಿಸುವ ಮೂಲಕ ನೀವು ಮಾಹಿತಿಯನ್ನು ಹಂಚಿಕೊಂಡಿರುವಿರಿ ಎಂದು ನಾವು ಭಾವಿಸುತ್ತೇವೆ. ನಿಮ್ಮನ್ನು ಬೆಂಬಲಿಸಲು ನಾವಿದ್ದೇವೆ. ಯಾವುದೇ ಹೆಚ್ಚಿನ ಸಮಸ್ಯೆ ಅಥವಾ ಸಲಹೆಗಾಗಿ ನೀವು ಇನಾಚೆ ಸಂಖ್ಯೆ {#var#} ಅನ್ನು ಸಂಪರ್ಕಿಸಬಹುದು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Miscellaneous Case-1/ Hindi",
        "TempId": "1707164622138672769",
        "body": "ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। आपका केस नंबर {#var#} बंद कर दिया गया है। कृपया इस संदेश का जवाब ना दें। Shahi प्रबंधन",
    },
    {
        "Title": "Miscellaneous Case-1/ Kannada",
        "TempId": "1707164622263982366",
        "body": "ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ನಿಮ್ಮ ಕೇಸ್ ಸಂಖ್ಯೆ {#var#} ಅನ್ನು ಮುಕ್ತಾಯಗೊಳಿಸಲಾಗಿದೆ. ದಯವಿಟ್ಟು ಈ ಸಂದೇಶಕ್ಕೆ ಪ್ರತಿಕ್ರಿಯಿಸಬೇಡಿ. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Miscellaneous Case-2/ Hindi",
        "TempId": "1707164622141826607",
        "body": "हमें 2 कार्य दिनों के भीतर आपकी तरफ से कोई प्रतिक्रिया नहीं मिली है। इसलिए आपका केस नंबर {#var#} बंद कर दिया गया है। कृपया इस संदेश का जवाब ना दें। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Miscellaneous Case-2/ Kannada",
        "TempId": "1707164622266571335",
        "body": "ನಿಮ್ಮಿಂದ ಎರಡು ಕೆಲಸದ ದಿನಗಳಲ್ಲಿ ಯಾವುದೇ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ನಮಗೆ ಕಳುಹಿಸಿಲ್ಲ. ಆದ್ದರಿಂದ, ನಿಮ್ಮ ಪ್ರಕರಣ ಸಂಖ್ಯೆ {#var#} ಅನ್ನು ಮುಕ್ತಾಯಗೊಳಿಸಲಾಗಿದೆ. ದಯವಿಟ್ಟು ಈ ಸಂದೇಶಕ್ಕೆ ಪ್ರತಿಕ್ರಿಯಿಸಬೇಡಿ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Acknowledgement of Complaint/ Hindi",
        "TempId": "1707164622146276709",
        "body": "आपका केस {#var#} विभाग को प्राप्त हो गया है। इसका जल्द से जल्द समाधान किया जाएगा। यदि हमें और किसी जानकारी की आवश्यकता होती है तो आपसे शीघ्र ही संपर्क किया जाएगा। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Acknowledgement of Complaint/ Kannada",
        "TempId": "1707164622269574109",
        "body": "ನಿಮ್ಮ ಸಮಸ್ಯೆಯನ್ನು {#var#} ಕಾರ್ಖಾನೆಯಲ್ಲಿ ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ನಾವು ಅದನ್ನು ಸಾಧ್ಯವಾದಷ್ಟು ಬೇಗ ಪರಿಹರಿಸುತ್ತೇವೆ. ನಮಗೆ ಏನಾದರೂ ಹೆಚ್ಚಿನ ವಿವರಗಳ ಅಗತ್ಯವಿದ್ದರೆ, ಶೀಘ್ರದಲ್ಲೇ ನಿಮ್ಮನ್ನು ಸಂಪರ್ಕಿಸಲಾಗುವುದು. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Acknowledgement of Query/ Hindi",
        "TempId": "1707164622149749742",
        "body": "आपका केस {#var#} विभाग को प्राप्त हो गया है। इसका जल्द से जल्द समाधान किया जाएगा। यदि हमें और किसी जानकारी की आवश्यकता होती है तो आपसे शीघ्र ही संपर्क किया जाएगा। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Acknowledgement of Suggestion/ Hindi",
        "TempId": "1707164622152845150",
        "body": "{#var#} पर सुझाव साझा करने के लिए आपका बहुत-बहुत धन्यवाद। हम संबंधित {#var#} के साथ इस पर चर्चा करेंगे और आपको बहुत जल्द ही सूचित करेंगे।ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Acknowledgement of Suggestion/ Kannada",
        "TempId": "1707164622278201133",
        "body": "{#var#} ನಲ್ಲಿ ನಿಮ್ಮ ಅಮೂಲ್ಯವಾದ ಸಲಹೆಯನ್ನು ಹಂಚಿಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ತುಂಬಾ ಧನ್ಯವಾದಗಳು. ನಾವು ಇದನ್ನು ಆಯಾ {#var#} ಜೊತೆಗೆ ಚರ್ಚಿಸುತ್ತೇವೆ ಮತ್ತು ಶೀಘ್ರದಲ್ಲೇ ನಿಮಗೆ ತಿಳಿಸುತ್ತೇನೆ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Requirement/ Hindi",
        "TempId": "1707164622156994996",
        "body": "आपका केस {#var#} विभाग में प्राप्त हो गया है। आपको बेहतर समर्थन देने के लिए हमें आपके {#var#} की जल्द से जल्द आवश्यकता होगी। कृपया यह आवश्यक जानकारी ईनाचे नंबर {#var#} पर भेजें। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Requirement-1/ Hindi",
        "TempId": "1707164622159204171",
        "body": "हमें आपका केस प्राप्त हो गया है। कृपया हमें विस्तार से बताएं कि समस्या कहां हुई है और यह आपको कैसे प्रभावित कर रही है। ईनाचे नंबर {#var#} पर जवाब दें। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Resolution/ Hindi",
        "TempId": "1707166928356735429",
        "body": "${aboutDetails} के बारे में आपके केस का समाधान कर दिया गया है। अगर आप समाधान से संतुष्ट हैं तो कृपया "
        "हां, मैं संतुष्ट हूं"
        " और अगर आप समाधान से संतुष्ट नहीं हैं तो "
        "नहीं, मैं सन्तुष्ट नहीं हूं"
        " कह के अपना वॉयस रिकॉड संदेश ${inacheNo} नंबर पर भेजें। कृपया इस संदेश का जवाब ना दें। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Resolution/ Kannada",
        "TempId": "1707166928351590500",
        "body": "${aboutDetails} ಕುರಿತ ನಿಮ್ಮ ಪ್ರಕರಣವನ್ನು ಪರಿಹರಿಸಲಾಗಿದೆ. ನೀವು ತೃಪ್ತರಾಗಿದ್ದರೆ "
        "ಹೌದು, ನಾನು ತೃಪ್ತಿ ಹೊಂದಿದ್ದೇನೆ"
        " ಅಥವಾ ನೀವು ನಿರ್ಣಯದಿಂದ ತೃಪ್ತರಾಗದಿದ್ದರೆ "
        "ಇಲ್ಲ, ನನಗೆ ತೃಪ್ತಿ ಇಲ್ಲ"
        " ಎಂದು ದಯವಿಟ್ಟು ಹೇಳಿ. ದಯವಿಟ್ಟು ಈ ಸಂದೇಶಕ್ಕೆ ಪ್ರತಿಕ್ರಿಯಿಸಬೇಡಿ. ನಿಮ್ಮ ಧ್ವನಿ-ರೆಕಾರ್ಡ್ ಮಾಡಿದ ಪ್ರತ್ಯುತ್ತರವನ್ನು ${inacheNo} ಗೆ ಕಳುಹಿಸಿ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ನಿರ್ವಹಣೆ",
    },
    {
        "Title": "Go to department/ Kannada",
        "TempId": "1707164622295101136",
        "body": "ನಿಮ್ಮ ಪ್ರಕರಣವನ್ನು ನಾವು ಸ್ವೀಕರಿಸಿದ್ದೇವೆ. ನಿಮ್ಮ ಪ್ರಕರಣವನ್ನು ಪರಿಹರಿಸಲು, ದಯವಿಟ್ಟು 2 ಕೆಲಸದ ದಿನಗಳಲ್ಲಿ {#var#} ವಿಭಾಗದಲ್ಲಿ {#var#} ಅನ್ನು ಭೇಟಿ ಮಾಡಿ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Go to department/ Hindi",
        "TempId": "1707164622164501989",
        "body": "हमें आपका केस प्राप्त हो गया है।। अपने मामले के समाधान के लिए कृपया आप {#var#} से {#var#} विभाग में 2 कार्य दिनों के अंदर मिले। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Lack of response/ Hindi",
        "TempId": "1707164622167225040",
        "body": "हमें 2 कार्य दिनों के भीतर आपकी और से कोई प्रतिक्रिया नहीं मिली। इसलिए आपका केस नंबर {#var#} बंद कर दिया गया है। कृपया इस संदेश का जवाब ना दें। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Lack of response/ Kannada",
        "TempId": "1707164622298728661",
        "body": "ನಿಮ್ಮ ಕಡೆಯಿಂದ ನಾವು ಯಾವುದೇ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು 2 ಕೆಲಸದ ದಿನಗಳಲ್ಲಿ ಸ್ವೀಕರಿಸಲಿಲ್ಲ. ಆದ್ದರಿಂದ ನಿಮ್ಮ ಕೇಸ್ ಸಂಖ್ಯೆ{#var#} ಅನ್ನು ಮುಕ್ತಾಯಗೊಳಿಸಲಾಗಿದೆ. ದಯವಿಟ್ಟು ಈ ಸಂದೇಶಕ್ಕೆ ಪ್ರತಿಕ್ರಿಯಿಸಬೇಡಿ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "General case/ Hindi",
        "TempId": "1707164622170468348",
        "body": "इस मुद्दे के बारे में हमें सूचित करने के लिए आपका बहुत-बहुत धन्यवाद। {#var#}। हम जल्द से जल्द इस समस्या का समाधान करेंगे। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Special case/ Hindi",
        "TempId": "1707164622173143931",
        "body": "ईनाचे के माध्यम से हमें इस गंभीर मुद्दे के बारे में सूचित करने के लिए आपका बहुत-बहुत धन्यवाद। हम इस समस्या का जल्द से जल्द समाधान करेंगे। ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। Shahi प्रबंधन",
    },
    {
        "Title": "Special case/ Kannada",
        "TempId": "1707164622335724710",
        "body": "ಈ ಗಂಭೀರ ಸಮಸ್ಯೆಯನ್ನು ಇನಾಚೆ ಮೂಲಕ ನಮಗೆ ತಿಳಿಸಿದ್ದಕ್ಕಾಗಿ ತುಂಬಾ ಧನ್ಯವಾದಗಳು. ಆದಷ್ಟು ಬೇಗ ನಾವು ಈ ಸಮಸ್ಯೆಯನ್ನು ಪರಿಹರಿಸುತ್ತೇವೆ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Closing the case/ Kannada",
        "TempId": "1707164622338276880",
        "body": "ಕೇಸ್ ಸಂಖ್ಯೆ {#var#} ನೊಂದಿಗೆ {#var#} ಕುರಿತು ನಿಮ್ಮ ಸಮಸ್ಯೆಯನ್ನು ಮುಕ್ತಾಯಗೊಳಿಸಲಾಗಿದೆ.ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ದಯವಿಟ್ಟು ಈ ಸಂದೇಶಕ್ಕೆ ಪ್ರತಿಕ್ರಿಯಿಸಬೇಡಿ. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Closing the case/ Hindi",
        "TempId": "1707164622175922322",
        "body": "आपके {#var#} के मुद्दे से जुड़ा केस नंबर {#var#} बंद कर दिया गया है।ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। कृपया इस संदेश का जवाब ना दें। Shahi प्रबंधन",
    },
    {
        "Title": "Case registration acknowledgement/ Hindi",
        "TempId": "1707164622178353143",
        "body": "ईनाचे सेवा का उपयोग करने के लिए धन्यवाद। आपका केस नंबर {#var#} है। कृपया इस संदेश का जवाब ना दें। ईनाचे नंबर {#var#} पर अपना जवाब भेजें। Shahi प्रबंधन",
    },
    {
        "Title": "Acknowledgement of Query/ Kannada",
        "TempId": "1707164812010927618",
        "body": "{#var#} ಕುರಿತು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿದ್ದಕ್ಕಾಗಿ ತುಂಬಾ ಧನ್ಯವಾದಗಳು. ಇದನ್ನು {#var#} ವಿಭಾಗಕ್ಕೆ ನಿಯೋಜಿಸಲಾಗಿದೆ. ನಾವು ನಿಮಗೆ ಶೀಘ್ರದಲ್ಲೇ ತಿಳಿಸುತ್ತೇವೆ. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Requirement/ Kannada",
        "TempId": "1707164812013964577",
        "body": "ನಿಮ್ಮ ಪ್ರಕರಣವನ್ನು {#var#} ಕಾರ್ಖಾನೆಯಲ್ಲಿ ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ನಿಮ್ಮನ್ನು ಉತ್ತಮವಾಗಿ ಬೆಂಬಲಿಸಲು, ನಮಗೆ ನಿಮ್ಮ {#var#} ಅಗತ್ಯವಿದೆ. ದಯವಿಟ್ಟು ಈ ಸಂದೇಶಕ್ಕೆ ಪ್ರತಿಕ್ರಿಯಿಸಬೇಡಿ. ಇನಾಚೆ ಸಂಖ್ಯೆಗೆ ಉತ್ತರಿಸಿ {#var#}. ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Requirement-1/ Kannada",
        "TempId": "1707164812016972288",
        "body": "ನಿಮ್ಮ ಪ್ರಕರಣವನ್ನು ನಾವು ಸ್ವೀಕರಿಸಿದ್ದೇವೆ. ಸಮಸ್ಯೆ ಎಲ್ಲಿ ಸಂಭವಿಸಿದೆ ಮತ್ತು ಅದು ಹೇಗೆ ಪರಿಣಾಮ ಬೀರಿದೆ ಎಂಬುದನ್ನು ದಯವಿಟ್ಟು ನೀವು ನಮಗೆ ವಿವರವಾಗಿ ತಿಳಿಸಿ. ದಯವಿಟ್ಟು ಈ ಸಂದೇಶಕ್ಕೆ ಪ್ರತಿಕ್ರಿಯಿಸಬೇಡಿ. ಇನಾಚೆ ಸಂಖ್ಯೆಗೆ {#var#} ಉತ್ತರಿಸಿ . ಇನಾಚೆ ಸೇವೆ ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Case registration acknowledgement/ Kannada",
        "TempId": "1707164812019916378",
        "body": "ನಿಮ್ಮ ಕೇಸ್ ಸಂಖ್ಯೆ {#var#}, ಇನಾಚೆ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ದಯವಿಟ್ಟು ಈ ಸಂದೇಶಕ್ಕೆ ಪ್ರತಿಕ್ರಿಯಿಸಬೇಡಿ. ನಿಮ್ಮ ಉತ್ತರವನ್ನು ಇನಾಚೆ ಸಂಖ್ಯೆಗೆ {#var#} ಕಳುಹಿಸಿ. Shahi ಮ್ಯಾನೇಜ್ಮೆಂಟ್",
    },
    {
        "Title": "Benefit of government scheme/ Hindi",
        "TempId": "1707164812023037920",
        "body": "सरकार ने {#var#} समूह के लोगों के लिए {#var#} योजना शुरू की है। पात्र लाभार्थियों से अनुरोध है कि इस योजना का लाभ लेने के लिए {#var#} पर/में जाएं। Shahi प्रबंधन",
    },
    {
        "Title": "Benefit of government scheme/ English",
        "TempId": "1707164812026233209",
        "body": "Government has launched {#var#} scheme for {#var#} group of people. The eligible beneficiaries are requested to visit {#var#} to take benefit of this scheme. Shahi Management.",
    },
    {
        "Title": "Lack of response/ English",
        "TempId": "1707164621554841816",
        "body": "Since we did not receive any response from your side within 2 working days. Therefore, your case number{#var#} has been closed. Please Do Not respond to this message. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Requirement-1/ English",
        "TempId": "1707164621546507271",
        "body": "We have received your case. Kindly tell us in detail where the issue has occurred and how it has been impacting you. Reply on the Inache number {#var#}. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Employee vaccination/ English",
        "TempId": "1707164621589208676",
        "body": "{#var#} in collaboration with {#var#} hospital has organized free covid vaccine {#var#} for all employees. Those interested are hereby requested to bring your Aadhar card and get vaccinated between {#var#} to {#var#} in the factory. Shahi Management",
    },
    {
        "Title": "Emergency/Unprecedented event/ English",
        "TempId": "1707164621597753308",
        "body": "Owing to the issue of {#var#}, {#var#} department/facility would not be active for {#var#} no. of days from {#var#}. Shahi Management.",
    },
    {
        "Title": "Promotions and increments/ English",
        "TempId": "1707164621611211757",
        "body": "Everyone is informed that in the coming {#var#} days; promotions and Increments will be announced by the HR department. Kindly be informed. Please DO NOT respond to this message. Thank you for using Inache Service. Shahi Management.",
    },
    {
        "Title": "Health check up camp/ English",
        "TempId": "1707164621614186872",
        "body": "From {#var#} to {#var#} days/date; health check up camps will be organized by the health department. All of you are requested to visit the camps from {#var#} to {#var#} time. Kindly meet your respective reporting officers for further details. Please DO NOT respond to this message. Thank you for using Inache Service. Shahi Management.",
    },
    {
        "Title": "Awareness sessions/ English",
        "TempId": "1707164621616949951",
        "body": "{#var#} department is going to organize an awareness camp about {#var#} on {#var#} day/date from {#var#} to {#var#} time. All of you are required to attend this session. Kindly meet your respective reporting officers for your timings. Please DO NOT respond to this message. Thank you for using Inache Service. Shahi Management.",
    },
    {
        "Title": "Content of voice call-1/ English",
        "TempId": "1707164620323100685",
        "body": "Your voice is not clear. Kindly call again on the Inache number {#var#} and share your concern clearly after the beep sound. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Content of voice call-2/ English",
        "TempId": "1707164621428995672",
        "body": "Your voice call message is lacking the required information about your concern. Kindly call again on the Inache number {#var#} and explain in details. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Content of SMS/ English",
        "TempId": "1707164621440701744",
        "body": "Your SMS is lacking proper information relating to your issue. Kindly resend it with full information. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Miscellaneous Case-1/ English",
        "TempId": "1707164621521862589",
        "body": "Thank you for using the Inache service. Your case number {#var#} has been closed. Please Do Not respond to this message. Shahi Management",
    },
    {
        "Title": "Miscellaneous Case-2/ English",
        "TempId": "1707164621525121935",
        "body": "Since we did not receive any response from your side within 2 working days. Therefore, your case number{#var#} has been closed. Please Do Not respond to this message. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Acknowledgement of Complaint/ English",
        "TempId": "1707164621529440895",
        "body": "Your case has been received at {#var#} department. We will solve it as soon as possible. In case we need any further details, you will be contacted soon. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Acknowledgement of Suggestion/ English",
        "TempId": "1707164621537114865",
        "body": "Thank you very much for sharing your valuable suggestion on {#var#}. We will discuss this with the respective {#var#} and update you very soon. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Go to department/ English",
        "TempId": "1707164621552256400",
        "body": "We have received your case. To proceed further to resolve your case, kindly meet {#var#} in the {#var#} department within 2 working days. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "General case/ English",
        "TempId": "1707164621558617350",
        "body": "Thank you very much for informing us about this issue. {#var#}. We will resolve this problem as soon as possible. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Special case/ English",
        "TempId": "1707164621561229340",
        "body": "Thank you very much for informing us about this serious issue through Inache. We will resolve this problem as soon as possible. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Closing the case/ English",
        "TempId": "1707164621564408086",
        "body": "Your issue about {#var#} with case number {#var#} has been closed. Thank you for using Inache Service. Please Do Not respond to this message. Shahi Management",
    },
    {
        "Title": "Acknowledgement of Query/ English",
        "TempId": "1707164812004408664",
        "body": "Thank you very much for sharing your query about {#var#}. It has been assigned to {#var#} department. You will be notified soon. Thank you for using Inache Service. Shahi Management",
    },
    {
        "Title": "Requirement/ English",
        "TempId": "1707164812007972800",
        "body": "Your case has been received at {#var#} department. To support you better, we would need your {#var#} at the earliest. Thank you for using the Inache service. Please send this crucial information on the Inache number {#var#}. Shahi Management",
    },
    {
        "Title": "Changes in timing of work and shifts/ English",
        "TempId": "1707164852942846916",
        "body": "From {#var#} onwards; the timing of the work as well as the timing of the shifts has been changed. You are requested to see or visit {#var#} for full information.",
    },
]

employee_data = data

# now we will open a file for writing
data_file = open("data_file.csv", "w")

# create the csv writer object
csv_writer = csv.writer(data_file)

# Counter variable used for writing
# headers to the CSV file
count = 0

for emp in employee_data:
    if count == 0:

        # Writing headers of CSV file
        header = emp.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(emp.values())

data_file.close()
