"""Builds the support (index.html) and privacy (privacy.html) pages in every app language from one template.

English stays at the site root, because App Store Connect links there; other languages live in /<code>/.
Run from the repository root: python3 -I tools/build_pages.py
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EMAIL = "lenityapp@gmail.com"
LANGS = ["en", "es", "pt-BR", "de", "fr", "cs", "ja", "ko", "zh-Hans", "zh-Hant"]
NATIVE = {"en": "English", "es": "Español", "pt-BR": "Português (Brasil)", "de": "Deutsch", "fr": "Français",
          "cs": "Čeština", "ja": "日本語", "ko": "한국어", "zh-Hans": "简体中文", "zh-Hant": "繁體中文"}

# Store name, Home Screen name, then every sentence. Store and Home Screen names match the app and App Store Connect.
T = {
"en": dict(
    store="Remove Background Noise: Video", home="Remove Noise",
    support="Support", privacy="Privacy Policy",
    intro="{store} cleans up the voice in your videos and audio recordings, right on your iPhone or iPad. On your Home Screen it appears as “{home}”.",
    contact_h="Contact", contact="Questions, problems or ideas: {mail}. Tell us your device and iOS version if something doesn't work.",
    files_h="Which files can I open?", files="Videos from Photos or Files, and audio files in MP3, M4A or WAV from Files.",
    upload_h="Does the app upload my videos?", upload="No. Everything is processed on your device, and the app works without an internet connection.",
    photos_h="Why does it ask to access Photos?", photos="Only when you save a result. The app asks to add the new video to your library and never reads the rest of it.",
    price_h="Does it cost anything?", price="No. No ads, no subscriptions, no account.",
    effective="Effective 6 November 2026 for the {store} app (“{home}” on the Home Screen) for iPhone and iPad. It is made by Veronika Zelinkova, contact {mail}.",
    summary_h="Summary", summary="The app does not collect any personal data and does not send anything anywhere. It has no account, no ads, no analytics and no tracking.",
    media_h="Your videos and audio", media="Videos and audio files you open in the app are processed entirely on your device. They are never uploaded, and we have no access to them. A working copy and temporary files stay in the app’s own storage until you start a new clip or delete the app.",
    pick_h="Photos and Files", pick="You choose which videos and audio files to open with the system photo picker or the Files app, so the app sees only what you select. If you save a result to your photo library, the app asks for permission to add to it. It never reads your library.",
    prefs_h="Settings on your device", prefs="The app remembers two small things on your device: whether you have tried the touch-and-hold tip, and how many results you have saved and when it last asked you to rate the app. They never leave your device and are deleted with the app.",
    mail_h="Contacting us", mail_p="If you e-mail us, we receive your e-mail address and your message and use them only to reply.",
    third_h="Third parties", third="The app uses the open-source DeepFilterNet3 speech model and Apple’s Voice Isolation, both of which run on your device and send nothing anywhere. There are no third-party services, SDKs or trackers. Apple distributes the app through the App Store under its own privacy policy.",
    kids_h="Children", kids="The app collects no data from anyone, including children.",
    change_h="Changes", change="If this policy changes, we will update this page and the date at the top.",
    langs="Languages"),
"es": dict(
    store="Quitar Ruido de Fondo: Video", home="Quitar ruido",
    support="Soporte", privacy="Política de privacidad",
    intro="{store} limpia la voz de tus videos y grabaciones de audio, directamente en tu iPhone o iPad. En tu pantalla de inicio aparece como “{home}”.",
    contact_h="Contacto", contact="Preguntas, problemas o ideas: {mail}. Si algo no funciona, indícanos tu dispositivo y tu versión de iOS.",
    files_h="¿Qué archivos puedo abrir?", files="Videos de Fotos o de Archivos, y archivos de audio MP3, M4A o WAV de Archivos.",
    upload_h="¿La app sube mis videos?", upload="No. Todo se procesa en tu dispositivo y la app funciona sin conexión a internet.",
    photos_h="¿Por qué pide acceso a Fotos?", photos="Solo cuando guardas un resultado. La app pide permiso para añadir el nuevo video a tu fototeca y nunca lee el resto.",
    price_h="¿Cuesta algo?", price="No. Sin anuncios, sin suscripciones, sin cuenta.",
    effective="Vigente desde el 6 de noviembre de 2026 para la app {store} (“{home}” en la pantalla de inicio) para iPhone y iPad. La crea Veronika Zelinkova, contacto {mail}.",
    summary_h="Resumen", summary="La app no recopila ningún dato personal y no envía nada a ningún sitio. No tiene cuenta, anuncios, analíticas ni seguimiento.",
    media_h="Tus videos y audios", media="Los videos y archivos de audio que abres en la app se procesan por completo en tu dispositivo. Nunca se suben y no tenemos acceso a ellos. Una copia de trabajo y los archivos temporales se quedan en el almacenamiento propio de la app hasta que empiezas un clip nuevo o eliminas la app.",
    pick_h="Fotos y Archivos", pick="Tú eliges qué videos y archivos de audio abrir con el selector de fotos del sistema o con la app Archivos, así que la app solo ve lo que seleccionas. Si guardas un resultado en tu fototeca, la app pide permiso para añadirlo. Nunca lee tu fototeca.",
    prefs_h="Ajustes en tu dispositivo", prefs="La app recuerda dos cosas pequeñas en tu dispositivo: si ya probaste el consejo de mantener pulsado y cuántos resultados has guardado y cuándo te pidió por última vez que la valores. Nunca salen de tu dispositivo y se borran con la app.",
    mail_h="Contactarnos", mail_p="Si nos escribes un correo, recibimos tu dirección y tu mensaje y solo los usamos para responderte.",
    third_h="Terceros", third="La app usa el modelo de voz de código abierto DeepFilterNet3 y Aislamiento de voz de Apple; ambos funcionan en tu dispositivo y no envían nada. No hay servicios, SDK ni rastreadores de terceros. Apple distribuye la app a través del App Store según su propia política de privacidad.",
    kids_h="Menores", kids="La app no recopila datos de nadie, tampoco de menores.",
    change_h="Cambios", change="Si esta política cambia, actualizaremos esta página y la fecha del principio.",
    langs="Idiomas"),
"pt-BR": dict(
    store="Remover Ruído de Fundo: Vídeo", home="Remover Ruído",
    support="Suporte", privacy="Política de Privacidade",
    intro="O {store} limpa a voz dos seus vídeos e gravações de áudio, direto no seu iPhone ou iPad. Na Tela de Início ele aparece como “{home}”.",
    contact_h="Contato", contact="Dúvidas, problemas ou ideias: {mail}. Se algo não funcionar, informe seu aparelho e sua versão do iOS.",
    files_h="Quais arquivos posso abrir?", files="Vídeos do app Fotos ou do app Arquivos, e arquivos de áudio MP3, M4A ou WAV do app Arquivos.",
    upload_h="O app envia meus vídeos?", upload="Não. Tudo é processado no seu aparelho, e o app funciona sem conexão com a internet.",
    photos_h="Por que ele pede acesso ao Fotos?", photos="Só quando você salva um resultado. O app pede para adicionar o novo vídeo à sua biblioteca e nunca lê o resto dela.",
    price_h="Custa alguma coisa?", price="Não. Sem anúncios, sem assinaturas, sem conta.",
    effective="Em vigor desde 6 de novembro de 2026 para o app {store} (“{home}” na Tela de Início) para iPhone e iPad. Criado por Veronika Zelinkova, contato {mail}.",
    summary_h="Resumo", summary="O app não coleta nenhum dado pessoal e não envia nada para lugar nenhum. Não tem conta, anúncios, análises nem rastreamento.",
    media_h="Seus vídeos e áudios", media="Os vídeos e arquivos de áudio que você abre no app são processados inteiramente no seu aparelho. Eles nunca são enviados, e não temos acesso a eles. Uma cópia de trabalho e arquivos temporários ficam no armazenamento do próprio app até você começar um novo clipe ou apagar o app.",
    pick_h="Fotos e Arquivos", pick="Você escolhe quais vídeos e arquivos de áudio abrir com o seletor de fotos do sistema ou com o app Arquivos, então o app vê só o que você seleciona. Se você salvar um resultado na sua biblioteca de fotos, o app pede permissão para adicioná-lo. Ele nunca lê sua biblioteca.",
    prefs_h="Ajustes no seu aparelho", prefs="O app guarda duas pequenas informações no seu aparelho: se você já testou a dica de tocar e segurar, e quantos resultados você salvou e quando ele pediu pela última vez que você avaliasse o app. Elas nunca saem do seu aparelho e são apagadas com o app.",
    mail_h="Fale conosco", mail_p="Se você nos enviar um e-mail, recebemos seu endereço e sua mensagem e os usamos só para responder.",
    third_h="Terceiros", third="O app usa o modelo de voz de código aberto DeepFilterNet3 e o Isolamento de Voz da Apple; ambos rodam no seu aparelho e não enviam nada. Não há serviços, SDKs nem rastreadores de terceiros. A Apple distribui o app pela App Store segundo a própria política de privacidade.",
    kids_h="Crianças", kids="O app não coleta dados de ninguém, inclusive de crianças.",
    change_h="Alterações", change="Se esta política mudar, atualizaremos esta página e a data no topo.",
    langs="Idiomas"),
"de": dict(
    store="Hintergrundgeräusche entfernen", home="Entrauschen",
    support="Support", privacy="Datenschutzerklärung",
    intro="{store} säubert die Stimme in deinen Videos und Audioaufnahmen, direkt auf deinem iPhone oder iPad. Auf dem Home-Bildschirm heißt die App „{home}“.",
    contact_h="Kontakt", contact="Fragen, Probleme oder Ideen: {mail}. Wenn etwas nicht funktioniert, nenne uns bitte dein Gerät und deine iOS-Version.",
    files_h="Welche Dateien kann ich öffnen?", files="Videos aus Fotos oder Dateien sowie Audiodateien im Format MP3, M4A oder WAV aus Dateien.",
    upload_h="Lädt die App meine Videos hoch?", upload="Nein. Alles wird auf deinem Gerät verarbeitet, und die App funktioniert ohne Internetverbindung.",
    photos_h="Warum fragt sie nach Zugriff auf Fotos?", photos="Nur wenn du ein Ergebnis sicherst. Die App bittet darum, das neue Video zu deiner Mediathek hinzuzufügen, und liest den Rest nie.",
    price_h="Kostet die App etwas?", price="Nein. Keine Werbung, kein Abo, kein Konto.",
    effective="Gültig ab 6. November 2026 für die App {store} („{home}“ auf dem Home-Bildschirm) für iPhone und iPad. Sie stammt von Veronika Zelinkova, Kontakt {mail}.",
    summary_h="Zusammenfassung", summary="Die App erhebt keine personenbezogenen Daten und sendet nichts irgendwohin. Sie hat kein Konto, keine Werbung, keine Analyse und kein Tracking.",
    media_h="Deine Videos und Aufnahmen", media="Videos und Audiodateien, die du in der App öffnest, werden vollständig auf deinem Gerät verarbeitet. Sie werden nie hochgeladen, und wir haben keinen Zugriff darauf. Eine Arbeitskopie und temporäre Dateien bleiben im eigenen Speicher der App, bis du einen neuen Clip beginnst oder die App löschst.",
    pick_h="Fotos und Dateien", pick="Du wählst selbst, welche Videos und Audiodateien du über die Fotoauswahl des Systems oder die Dateien-App öffnest. Die App sieht also nur, was du auswählst. Wenn du ein Ergebnis in deiner Mediathek sicherst, fragt die App um Erlaubnis, es hinzuzufügen. Sie liest deine Mediathek nie.",
    prefs_h="Einstellungen auf deinem Gerät", prefs="Die App merkt sich zwei Kleinigkeiten auf deinem Gerät: ob du den Tipp zum Gedrückthalten schon ausprobiert hast, und wie viele Ergebnisse du gesichert hast und wann sie zuletzt um eine Bewertung gebeten hat. Diese Angaben verlassen dein Gerät nie und werden mit der App gelöscht.",
    mail_h="Kontakt per E-Mail", mail_p="Wenn du uns eine E-Mail schreibst, erhalten wir deine Adresse und deine Nachricht und nutzen sie nur für die Antwort.",
    third_h="Dritte", third="Die App nutzt das Open-Source-Sprachmodell DeepFilterNet3 und Apples Sprachisolation. Beide laufen auf deinem Gerät und senden nichts. Es gibt keine Dienste, SDKs oder Tracker von Dritten. Apple vertreibt die App über den App Store nach eigener Datenschutzrichtlinie.",
    kids_h="Kinder", kids="Die App erhebt von niemandem Daten, auch nicht von Kindern.",
    change_h="Änderungen", change="Wenn sich diese Erklärung ändert, aktualisieren wir diese Seite und das Datum oben.",
    langs="Sprachen"),
"fr": dict(
    store="Supprimer Bruit de Fond: Vidéo", home="Anti-bruit",
    support="Assistance", privacy="Politique de confidentialité",
    intro="{store} nettoie la voix de vos vidéos et enregistrements audio, directement sur votre iPhone ou iPad. Sur l’écran d’accueil, elle s’appelle « {home} ».",
    contact_h="Contact", contact="Questions, problèmes ou idées : {mail}. Si quelque chose ne fonctionne pas, indiquez-nous votre appareil et votre version d’iOS.",
    files_h="Quels fichiers puis-je ouvrir ?", files="Des vidéos de Photos ou de Fichiers, et des fichiers audio MP3, M4A ou WAV de Fichiers.",
    upload_h="L’app envoie-t-elle mes vidéos ?", upload="Non. Tout est traité sur votre appareil, et l’app fonctionne sans connexion internet.",
    photos_h="Pourquoi demande-t-elle l’accès à Photos ?", photos="Uniquement quand vous enregistrez un résultat. L’app demande à ajouter la nouvelle vidéo à votre photothèque et ne lit jamais le reste.",
    price_h="Est-ce payant ?", price="Non. Pas de publicité, pas d’abonnement, pas de compte.",
    effective="En vigueur à partir du 6 novembre 2026 pour l’app {store} (« {home} » sur l’écran d’accueil) pour iPhone et iPad. Elle est créée par Veronika Zelinkova, contact {mail}.",
    summary_h="En bref", summary="L’app ne collecte aucune donnée personnelle et n’envoie rien nulle part. Elle n’a ni compte, ni publicité, ni statistiques, ni suivi.",
    media_h="Vos vidéos et audios", media="Les vidéos et fichiers audio que vous ouvrez dans l’app sont traités entièrement sur votre appareil. Ils ne sont jamais envoyés et nous n’y avons pas accès. Une copie de travail et des fichiers temporaires restent dans le stockage de l’app jusqu’à ce que vous commenciez un nouveau clip ou supprimiez l’app.",
    pick_h="Photos et Fichiers", pick="Vous choisissez les vidéos et fichiers audio à ouvrir avec le sélecteur de photos du système ou l’app Fichiers : l’app ne voit que ce que vous sélectionnez. Si vous enregistrez un résultat dans votre photothèque, l’app demande l’autorisation de l’y ajouter. Elle ne lit jamais votre photothèque.",
    prefs_h="Réglages sur votre appareil", prefs="L’app retient deux petites choses sur votre appareil : si vous avez déjà essayé l’astuce de l’appui prolongé, et combien de résultats vous avez enregistrés et quand elle vous a demandé de la noter pour la dernière fois. Elles ne quittent jamais votre appareil et sont effacées avec l’app.",
    mail_h="Nous écrire", mail_p="Si vous nous écrivez, nous recevons votre adresse e-mail et votre message et ne les utilisons que pour vous répondre.",
    third_h="Tiers", third="L’app utilise le modèle vocal open source DeepFilterNet3 et l’Isolation de la voix d’Apple ; tous deux fonctionnent sur votre appareil et n’envoient rien. Il n’y a aucun service, SDK ou traceur tiers. Apple distribue l’app sur l’App Store selon sa propre politique de confidentialité.",
    kids_h="Enfants", kids="L’app ne collecte de données sur personne, enfants compris.",
    change_h="Modifications", change="Si cette politique change, nous mettrons à jour cette page et la date en haut.",
    langs="Langues"),
"cs": dict(
    store="Odstranit šum: Video a zvuk", home="Odstranit šum",
    support="Podpora", privacy="Zásady ochrany soukromí",
    intro="{store} vyčistí hlas ve vašich videích a zvukových nahrávkách přímo v iPhonu nebo iPadu. Na ploše se jmenuje „{home}“.",
    contact_h="Kontakt", contact="Dotazy, problémy nebo nápady: {mail}. Když něco nefunguje, napište nám své zařízení a verzi iOS.",
    files_h="Jaké soubory můžu otevřít?", files="Videa z Fotek nebo Souborů a zvukové soubory MP3, M4A nebo WAV ze Souborů.",
    upload_h="Nahrává aplikace moje videa?", upload="Ne. Všechno se zpracuje ve vašem zařízení a aplikace funguje i bez internetu.",
    photos_h="Proč žádá o přístup k Fotkám?", photos="Jen když ukládáte výsledek. Aplikace žádá o přidání nového videa do knihovny a zbytek nikdy nečte.",
    price_h="Stojí něco?", price="Ne. Žádné reklamy, žádné předplatné, žádný účet.",
    effective="Platí od 6. listopadu 2026 pro aplikaci {store} („{home}“ na ploše) pro iPhone a iPad. Autorkou je Veronika Zelinková, kontakt {mail}.",
    summary_h="Shrnutí", summary="Aplikace nesbírá žádné osobní údaje a nikam nic neposílá. Nemá účet, reklamy, analytiku ani sledování.",
    media_h="Vaše videa a nahrávky", media="Videa a zvukové soubory, které v aplikaci otevřete, se zpracují celé ve vašem zařízení. Nikdy se nenahrávají a my k nim nemáme přístup. Pracovní kopie a dočasné soubory zůstávají v úložišti aplikace, dokud nezačnete nový klip nebo aplikaci nesmažete.",
    pick_h="Fotky a Soubory", pick="Sami vybíráte, která videa a zvukové soubory otevřete přes systémový výběr fotek nebo aplikaci Soubory, takže aplikace vidí jen to, co vyberete. Když uložíte výsledek do knihovny fotek, aplikace požádá o svolení ho přidat. Vaši knihovnu nikdy nečte.",
    prefs_h="Nastavení ve vašem zařízení", prefs="Aplikace si ve vašem zařízení pamatuje dvě drobnosti: jestli jste už vyzkoušeli tip s podržením prstu, a kolik výsledků jste uložili a kdy naposledy požádala o hodnocení. Nikdy neopustí vaše zařízení a smažou se spolu s aplikací.",
    mail_h="Když nám napíšete", mail_p="Když nám pošlete e-mail, dostaneme vaši adresu a zprávu a použijeme je jen k odpovědi.",
    third_h="Třetí strany", third="Aplikace používá open-source hlasový model DeepFilterNet3 a Izolaci hlasu od Applu; oba běží ve vašem zařízení a nic neposílají. Nejsou v ní žádné služby, SDK ani sledovací nástroje třetích stran. Apple aplikaci distribuuje přes App Store podle vlastních zásad ochrany soukromí.",
    kids_h="Děti", kids="Aplikace nesbírá údaje od nikoho, ani od dětí.",
    change_h="Změny", change="Když se tyto zásady změní, aktualizujeme tuto stránku a datum nahoře.",
    langs="Jazyky"),
"ja": dict(
    store="ノイズ除去：動画と録音の雑音を消す", home="ノイズ除去",
    support="サポート", privacy="プライバシーポリシー",
    intro="{store}は、動画や録音の声を iPhone や iPad の上でそのままクリーンにします。ホーム画面では「{home}」と表示されます。",
    contact_h="お問い合わせ", contact="ご質問、不具合、ご意見は {mail} まで。うまく動かない場合は、お使いのデバイスと iOS のバージョンをお知らせください。",
    files_h="どんなファイルを開けますか？", files="「写真」または「ファイル」の動画と、「ファイル」の MP3、M4A、WAV の音声ファイルです。",
    upload_h="動画はアップロードされますか？", upload="いいえ。すべてデバイス上で処理され、インターネットに接続していなくても使えます。",
    photos_h="なぜ「写真」へのアクセスを求めるのですか？", photos="結果を保存するときだけです。新しい動画をライブラリに追加する許可を求めるだけで、ほかの写真や動画を読むことはありません。",
    price_h="料金はかかりますか？", price="いいえ。広告なし、サブスクリプションなし、アカウント不要です。",
    effective="2026年11月6日発効。iPhone および iPad 用アプリ「{store}」（ホーム画面では「{home}」）に適用されます。開発者は Veronika Zelinkova、連絡先は {mail} です。",
    summary_h="概要", summary="このアプリは個人データを一切収集せず、どこにも何も送信しません。アカウント、広告、分析、トラッキングはありません。",
    media_h="動画と音声", media="アプリで開いた動画や音声ファイルは、すべてデバイス上で処理されます。アップロードされることはなく、私たちがアクセスすることもありません。作業用のコピーと一時ファイルは、新しいクリップを始めるかアプリを削除するまで、アプリ専用の領域に保存されます。",
    pick_h="「写真」と「ファイル」", pick="開く動画や音声ファイルは、システムの写真ピッカーまたは「ファイル」App でご自身が選ぶため、アプリが見るのは選んだものだけです。結果を写真ライブラリに保存するときは、追加の許可を求めます。ライブラリを読むことはありません。",
    prefs_h="デバイス上の設定", prefs="アプリはデバイス上に2つの小さな情報だけを記録します。長押しのヒントを試したかどうかと、保存した結果の数および最後に評価をお願いした日時です。これらがデバイスの外に出ることはなく、アプリと一緒に削除されます。",
    mail_h="メールでのお問い合わせ", mail_p="メールをいただいた場合、メールアドレスと内容は返信のためだけに使用します。",
    third_h="第三者", third="アプリはオープンソースの音声モデル DeepFilterNet3 と Apple の声を分離を使用します。どちらもデバイス上で動作し、何も送信しません。第三者のサービス、SDK、トラッカーは含まれていません。アプリは Apple のプライバシーポリシーのもと App Store を通じて配信されます。",
    kids_h="お子様について", kids="このアプリは、お子様を含め、誰からもデータを収集しません。",
    change_h="変更について", change="このポリシーを変更する場合は、このページと冒頭の日付を更新します。",
    langs="言語"),
"ko": dict(
    store="노이즈 제거 - 동영상 배경 소음 제거", home="노이즈 제거",
    support="지원", privacy="개인정보 처리방침",
    intro="{store}는 동영상과 녹음 속 목소리를 iPhone이나 iPad에서 바로 깨끗하게 만듭니다. 홈 화면에서는 ‘{home}’(으)로 표시됩니다.",
    contact_h="문의", contact="질문, 문제, 아이디어: {mail}. 문제가 있으면 사용 중인 기기와 iOS 버전을 알려 주세요.",
    files_h="어떤 파일을 열 수 있나요?", files="사진 또는 파일 앱의 동영상, 그리고 파일 앱의 MP3, M4A, WAV 오디오 파일입니다.",
    upload_h="앱이 내 동영상을 업로드하나요?", upload="아니요. 모든 처리는 기기에서 이루어지며 인터넷 연결 없이도 작동합니다.",
    photos_h="왜 사진 접근 권한을 요청하나요?", photos="결과를 저장할 때만 요청합니다. 새 동영상을 보관함에 추가할 권한만 요청하며, 나머지는 절대 읽지 않습니다.",
    price_h="비용이 드나요?", price="아니요. 광고, 구독, 계정이 없습니다.",
    effective="2026년 11월 6일부터 iPhone 및 iPad용 앱 {store}(홈 화면의 ‘{home}’)에 적용됩니다. 개발자는 Veronika Zelinkova이며 연락처는 {mail}입니다.",
    summary_h="요약", summary="앱은 어떤 개인정보도 수집하지 않으며 아무 데도 아무것도 보내지 않습니다. 계정, 광고, 분석, 추적이 없습니다.",
    media_h="동영상과 오디오", media="앱에서 연 동영상과 오디오 파일은 모두 기기에서 처리됩니다. 업로드되지 않으며 저희는 접근할 수 없습니다. 작업용 사본과 임시 파일은 새 클립을 시작하거나 앱을 삭제할 때까지 앱 전용 저장 공간에 남습니다.",
    pick_h="사진과 파일", pick="열 동영상과 오디오 파일은 시스템 사진 선택기나 파일 앱에서 직접 고르므로 앱은 선택한 것만 볼 수 있습니다. 결과를 사진 보관함에 저장하면 추가 권한을 요청합니다. 보관함을 읽지는 않습니다.",
    prefs_h="기기에 저장되는 설정", prefs="앱은 기기에 작은 정보 두 가지만 기억합니다. 길게 누르기 팁을 사용해 봤는지, 그리고 저장한 결과 수와 마지막으로 평가를 요청한 시점입니다. 이 정보는 기기를 벗어나지 않으며 앱과 함께 삭제됩니다.",
    mail_h="이메일 문의", mail_p="이메일을 보내 주시면 이메일 주소와 메시지를 받아 답장에만 사용합니다.",
    third_h="제3자", third="앱은 오픈 소스 음성 모델 DeepFilterNet3과 Apple의 음성 분리를 사용하며, 둘 다 기기에서 실행되고 아무것도 전송하지 않습니다. 제3자 서비스, SDK, 추적기는 없습니다. Apple은 자체 개인정보 처리방침에 따라 App Store에서 앱을 배포합니다.",
    kids_h="아동", kids="앱은 아동을 포함한 누구에게서도 데이터를 수집하지 않습니다.",
    change_h="변경", change="이 방침이 변경되면 이 페이지와 상단의 날짜를 업데이트합니다.",
    langs="언어"),
"zh-Hans": dict(
    store="降噪器：视频与录音去杂音", home="去除噪音",
    support="支持", privacy="隐私政策",
    intro="{store}可直接在 iPhone 或 iPad 上清理视频和录音中的人声。在主屏幕上它显示为“{home}”。",
    contact_h="联系我们", contact="问题、故障或建议：{mail}。如果出现问题，请告诉我们你的设备和 iOS 版本。",
    files_h="可以打开哪些文件？", files="“照片”或“文件”中的视频，以及“文件”中的 MP3、M4A 或 WAV 音频文件。",
    upload_h="App 会上传我的视频吗？", upload="不会。所有处理都在你的设备上完成，无需联网即可使用。",
    photos_h="为什么要求访问“照片”？", photos="仅在你存储结果时。App 只请求将新视频添加到你的图库，从不读取其他内容。",
    price_h="需要付费吗？", price="不需要。没有广告，没有订阅，无需账户。",
    effective="自 2026 年 11 月 6 日起适用于 iPhone 和 iPad 版 App“{store}”（主屏幕上显示为“{home}”）。开发者为 Veronika Zelinkova，联系方式 {mail}。",
    summary_h="概要", summary="本 App 不收集任何个人数据，也不向任何地方发送任何内容。没有账户、广告、分析或跟踪。",
    media_h="你的视频和音频", media="你在 App 中打开的视频和音频文件完全在你的设备上处理。它们从不上传，我们也无法访问。工作副本和临时文件保存在 App 自己的存储空间中，直到你开始新的片段或删除 App。",
    pick_h="“照片”和“文件”", pick="你通过系统照片选择器或“文件”App 自行选择要打开的视频和音频文件，因此 App 只能看到你选择的内容。如果你将结果存储到照片图库，App 会请求添加权限。它从不读取你的图库。",
    prefs_h="设备上的设置", prefs="App 只在你的设备上记住两项小信息：你是否已尝试过长按提示，以及你存储了多少个结果、上次请你评分的时间。这些信息从不离开你的设备，并会随 App 一起删除。",
    mail_h="发送邮件", mail_p="如果你给我们发邮件，我们会收到你的邮箱地址和消息，仅用于回复你。",
    third_h="第三方", third="App 使用开源语音模型 DeepFilterNet3 和 Apple 的语音突显，两者都在你的设备上运行，不发送任何内容。没有第三方服务、SDK 或跟踪器。Apple 依据其自身隐私政策通过 App Store 分发本 App。",
    kids_h="儿童", kids="本 App 不收集任何人的数据，包括儿童。",
    change_h="变更", change="如果本政策有变更，我们会更新此页面及顶部的日期。",
    langs="语言"),
"zh-Hant": dict(
    store="降噪器：影片與錄音去雜音", home="去除雜音",
    support="支援", privacy="隱私權政策",
    intro="{store}可直接在 iPhone 或 iPad 上清理影片和錄音中的人聲。在主畫面上它顯示為「{home}」。",
    contact_h="聯絡我們", contact="問題、故障或建議：{mail}。如果發生問題，請告訴我們你的裝置和 iOS 版本。",
    files_h="可以打開哪些檔案？", files="「照片」或「檔案」中的影片，以及「檔案」中的 MP3、M4A 或 WAV 音訊檔。",
    upload_h="App 會上傳我的影片嗎？", upload="不會。所有處理都在你的裝置上完成，不用連網也能使用。",
    photos_h="為什麼要求取用「照片」？", photos="只在你儲存結果時。App 只要求將新影片加入你的圖庫，從不讀取其他內容。",
    price_h="需要付費嗎？", price="不需要。沒有廣告，沒有訂閱，不需帳號。",
    effective="自 2026 年 11 月 6 日起適用於 iPhone 和 iPad 版 App「{store}」（主畫面上顯示為「{home}」）。開發者為 Veronika Zelinkova，聯絡方式 {mail}。",
    summary_h="摘要", summary="本 App 不收集任何個人資料，也不向任何地方傳送任何內容。沒有帳號、廣告、分析或追蹤。",
    media_h="你的影片和音訊", media="你在 App 中打開的影片和音訊檔完全在你的裝置上處理。它們從不上傳，我們也無法取用。工作副本和暫存檔會保存在 App 自己的儲存空間中，直到你開始新的片段或刪除 App。",
    pick_h="「照片」和「檔案」", pick="你透過系統照片選擇器或「檔案」App 自行選擇要打開的影片和音訊檔，因此 App 只能看到你選擇的內容。如果你將結果儲存到照片圖庫，App 會要求加入權限。它從不讀取你的圖庫。",
    prefs_h="裝置上的設定", prefs="App 只在你的裝置上記住兩項小資訊：你是否已試過長按提示，以及你儲存了多少個結果、上次請你評分的時間。這些資訊從不離開你的裝置，並會隨 App 一起刪除。",
    mail_h="寄送電子郵件", mail_p="如果你寄電子郵件給我們，我們會收到你的電子郵件地址和訊息，僅用於回覆你。",
    third_h="第三方", third="App 使用開源語音模型 DeepFilterNet3 和 Apple 的語音突顯，兩者都在你的裝置上執行，不傳送任何內容。沒有第三方服務、SDK 或追蹤器。Apple 依其隱私權政策透過 App Store 發行本 App。",
    kids_h="兒童", kids="本 App 不收集任何人的資料，包括兒童。",
    change_h="變更", change="如果本政策有變更，我們會更新此頁面及頂端的日期。",
    langs="語言"),
}

STYLE = """:root{--ink:#141414;--muted:#4D4D4D;--line:#E9E9E9;--accent:#73D9BF;--bg:#fff}
@media (prefers-color-scheme:dark){:root{--ink:#F2F2F2;--muted:#B5B5B5;--line:#2A2A2A;--bg:#141518}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:680px;margin:0 auto;padding:48px 20px 72px}
.brand{display:inline-block;background:var(--accent);color:#141414;font-weight:700;padding:4px 10px;border-radius:8px;font-size:14px}
h1{font-size:34px;line-height:1.1;letter-spacing:-.02em;margin:18px 0 8px}
h2{font-size:21px;margin:36px 0 8px}
p,li{color:var(--muted)}
a{color:var(--ink)}
.small{font-size:14px;margin-top:48px;border-top:1px solid var(--line);padding-top:16px}
.langs{font-size:14px;line-height:1.9}"""

BASE = "https://jojoch.github.io/denoise-web/"


def prefix(lang: str) -> str:
    return "" if lang == "en" else f"{lang}/"


def page(lang: str, kind: str) -> str:
    t = T[lang]
    up = "" if lang == "en" else "../"
    mail = f'<a href="mailto:{EMAIL}?subject=Remove%20Noise">{EMAIL}</a>'
    fill = lambda s: html.escape(s.format(store=t["store"], home=t["home"], mail="\x00")).replace("\x00", mail)
    title = t["support"] if kind == "index" else t["privacy"]
    if kind == "index":
        body = [f"<p>{fill(t['intro'])}</p>"]
        for key in ("contact", "files", "upload", "photos", "price"):
            body += [f"<h2>{html.escape(t[key + '_h'])}</h2>", f"<p>{fill(t[key])}</p>"]
    else:
        body = [f"<p>{fill(t['effective'])}</p>"]
        for key, text in (("summary", "summary"), ("media", "media"), ("pick", "pick"), ("prefs", "prefs"),
                          ("mail", "mail_p"), ("third", "third"), ("kids", "kids"), ("change", "change")):
            body += [f"<h2>{html.escape(t[key + '_h'])}</h2>", f"<p>{fill(t[text])}</p>"]
    alternates = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{prefix(l)}{kind}.html">' for l in LANGS)
    langs = " · ".join(
        (f"<strong>{NATIVE[l]}</strong>" if l == lang else f'<a href="{up}{prefix(l)}{kind}.html" lang="{l}">{NATIVE[l]}</a>')
        for l in LANGS)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t['store'])} – {html.escape(title)}</title>
{alternates}
<link rel="alternate" hreflang="x-default" href="{BASE}{kind}.html">
<style>
{STYLE}
</style>
</head>
<body>
<main>
<span class="brand">{html.escape(t['store'])}</span>
<h1>{html.escape(title)}</h1>
{chr(10).join(body)}
<p class="small"><a href="index.html">{html.escape(t['support'])}</a> · <a href="privacy.html">{html.escape(t['privacy'])}</a></p>
<p class="langs">{html.escape(t['langs'])}: {langs}</p>
</main>
</body>
</html>
"""


for lang in LANGS:
    folder = ROOT / prefix(lang)
    folder.mkdir(parents=True, exist_ok=True)
    for kind in ("index", "privacy"):
        (folder / f"{kind}.html").write_text(page(lang, kind), encoding="utf-8")
print("built", len(LANGS) * 2, "pages")
