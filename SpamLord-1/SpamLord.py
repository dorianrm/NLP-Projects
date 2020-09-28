import sys
import os
import re
import pprint
from io import open

# Gradescope: 23/24

phone_pat = [
    '([0-9]{3})[- ]([0-9]{3})[- ]([0-9]{4})' ,   #808-280-2339 or 808 280 2339

    '[(]([0-9]{3})[)][- ]?([0-9]{3})[- ]?([0-9]{4})' , #(808) 280-339
    '(?:[+1])([0-9]{3})([0-9]{3})([0-9]{4})' ,   #+18082802339
    '(?:[1])([0-9]{3})([0-9]{3})([0-9]{4})' ,    #18082802339
    '(?:[(]?[+]?[1][)]?)?[- ]?[(]([0-9]{3})[)][- ]?([0-9]{3})[- ]?([0-9]{4})'
 
]

email_pat = [
    #'(\w+)@(\w+).edu' ,

    #'([A-Za-z0-9._]+)(?:@| @ | at | WHERE |&#x40;)([A-Za-z0-9._;]+)(?: dot |\.| dt | DOM |;)(?:edu|EDU)' ,#&#x40; = @
    #'([A-Za-z0-9._]+)(?:@| @ | at | WHERE |&#x40;)([A-Za-z0-9._;]+)(?: dot |\.| dt | DOM |;)(?:com|COM)'
    '([\w\.-]+)(?:@| @ | at | WHERE |&#x40;|&#x40.)([\w\.;-]+)[\.|;]([\w-]+)' ,
    'obfuscate\(\'([\w\. -]+)\.([\w\.-]+)\',\'([\w\.-]+)\'' ,
    'email: ([\w; -]+)(?:@| @ | at | WHERE |&#x40;|&#x40.)([\w\.; -]+) ([\w-]+)'

]

# email_pat2 = [

#     #'([A-Za-z0-9._]+)(?:@| at | WHERE |&#x40;)([A-Za-z0-9._]+)(?:\.| dot | dt | DOM |;| )([A-Za-z0-9._]+)(?:\.| dot | dt | DOM |;| )(?:edu|com|EDU|COM)' , #jks case
#     #'([\w\.-]+)(?:@| @ | at | WHERE |&#x40;)([\w\.-]+)(?: dot |\.| dt | DOM |;)([\w\.-]+)(?: dot |\.| dt | DOM |;)([\w-]+)' ,
#     '([\w\.-]+)(?:@| @ | at | WHERE |&#x40;)([\w\.-]+)\.([\w\.-]+)\.([\w-]+)' ,

#     'obfuscate\(\'([\w\.-]+)\.([\w\.-]+)\',\'([\w\.-]+)\''
# # pal, jks, 3 words after @ sign cases,
# ]

# email_pat3 = [
#     '([\w\.-]+)(?: dot |\.| dt | DOM |;)([\w\.-]+)(?:@| @ | at | WHERE |&#x40;)([\w\.-]+)(?: dot |\.| dt | DOM |;)(?:edu|EDU)' ,
#     '([\w\.-]+)(?: dot |\.| dt | DOM |;)([\w\.-]+)(?:@| @ | at | WHERE |&#x40;)([\w\.-]+)(?: dot |\.| dt | DOM |;)(?:com|COM)'
# ]

# email_pat4 = [
#     '([\w\.-]+)(?: dot |\.| dt | DOM |;)([\w\.-]+)(?:@| @ | at | WHERE |&#x40;)([\w\.-]+)(?: dot |\.| dt | DOM |;)([\w\.-]+)(?: dot |\.| dt | DOM |;)(?:edu|EDU)' ,
#     '([\w\.-]+)(?: dot |\.| dt | DOM |;)([\w\.-]+)(?:@| @ | at | WHERE |&#x40;)([\w\.-]+)(?: dot |\.| dt | DOM |;)([\w\.-]+)(?: dot |\.| dt | DOM |;)(?:com|COM)'
# ]
# ([A-Za-z0-9._-]+) vs ([A-Za-z0-9._]+)  = no difference?


TLD = [
    "AAA","AARP","ABARTH","ABB","ABBOTT","ABBVIE","ABC","ABLE","ABOGADO","ABUDHABI","AC","ACADEMY","ACCENTURE","ACCOUNTANT","ACCOUNTANTS","ACO","ACTOR","AD","ADAC","ADS","ADULT","AE","AEG","AERO","AETNA","AF","AFAMILYCOMPANY","AFL","AFRICA","AG","AGAKHAN","AGENCY","AI","AIG","AIGO","AIRBUS","AIRFORCE","AIRTEL","AKDN","AL","ALFAROMEO","ALIBABA","ALIPAY","ALLFINANZ","ALLSTATE","ALLY","ALSACE","ALSTOM","AM","AMERICANEXPRESS","AMERICANFAMILY","AMEX","AMFAM","AMICA","AMSTERDAM","ANALYTICS","ANDROID","ANQUAN","ANZ","AO","AOL","APARTMENTS","APP","APPLE","AQ","AQUARELLE","AR","ARAB","ARAMCO","ARCHI","ARMY","ARPA","ART","ARTE","AS","ASDA","ASIA","ASSOCIATES","AT","ATHLETA","ATTORNEY","AU","AUCTION","AUDI","AUDIBLE","AUDIO","AUSPOST","AUTHOR","AUTO","AUTOS","AVIANCA","AW","AWS","AX","AXA","AZ","AZURE","BA","BABY","BAIDU","BANAMEX","BANANAREPUBLIC","BAND","BANK","BAR","BARCELONA","BARCLAYCARD","BARCLAYS","BAREFOOT","BARGAINS","BASEBALL","BASKETBALL","BAUHAUS","BAYERN","BB","BBC","BBT","BBVA","BCG","BCN","BD","BE","BEATS","BEAUTY","BEER","BENTLEY","BERLIN","BEST","BESTBUY","BET","BF","BG","BH","BHARTI","BI","BIBLE","BID","BIKE","BING","BINGO","BIO","BIZ","BJ","BLACK","BLACKFRIDAY","BLOCKBUSTER","BLOG","BLOOMBERG","BLUE","BM","BMS","BMW","BN","BNPPARIBAS","BO","BOATS","BOEHRINGER","BOFA","BOM","BOND","BOO","BOOK","BOOKING","BOSCH","BOSTIK","BOSTON","BOT","BOUTIQUE","BOX","BR","BRADESCO","BRIDGESTONE","BROADWAY","BROKER","BROTHER","BRUSSELS","BS","BT","BUDAPEST","BUGATTI","BUILD","BUILDERS","BUSINESS","BUY","BUZZ","BV","BW","BY","BZ","BZH","CA","CAB","CAFE","CAL","CALL","CALVINKLEIN","CAM","CAMERA","CAMP","CANCERRESEARCH","CANON","CAPETOWN","CAPITAL","CAPITALONE","CAR","CARAVAN","CARDS","CARE","CAREER","CAREERS","CARS","CASA","CASE","CASEIH","CASH","CASINO","CAT","CATERING","CATHOLIC","CBA","CBN","CBRE","CBS","CC","CD","CEB","CENTER","CEO","CERN","CF","CFA","CFD","CG","CH","CHANEL","CHANNEL","CHARITY","CHASE","CHAT","CHEAP","CHINTAI","CHRISTMAS","CHROME","CHURCH","CI","CIPRIANI","CIRCLE","CISCO","CITADEL","CITI","CITIC","CITY","CITYEATS","CK","CL","CLAIMS","CLEANING","CLICK","CLINIC","CLINIQUE","CLOTHING","CLOUD","CLUB","CLUBMED","CM","CN","CO","COACH","CODES","COFFEE","COLLEGE","COLOGNE","COM","COMCAST","COMMBANK","COMMUNITY","COMPANY","COMPARE","COMPUTER","COMSEC","CONDOS","CONSTRUCTION","CONSULTING","CONTACT","CONTRACTORS","COOKING","COOKINGCHANNEL","COOL","COOP","CORSICA","COUNTRY","COUPON","COUPONS","COURSES","CPA","CR","CREDIT","CREDITCARD","CREDITUNION","CRICKET","CROWN","CRS","CRUISE","CRUISES","CSC","CU","CUISINELLA","CV","CW","CX","CY","CYMRU","CYOU","CZ","DABUR","DAD","DANCE","DATA","DATE","DATING","DATSUN","DAY","DCLK","DDS","DE","DEAL","DEALER","DEALS","DEGREE","DELIVERY","DELL","DELOITTE","DELTA","DEMOCRAT","DENTAL","DENTIST","DESI","DESIGN","DEV","DHL","DIAMONDS","DIET","DIGITAL","DIRECT","DIRECTORY","DISCOUNT","DISCOVER","DISH","DIY","DJ","DK","DM","DNP","DO","DOCS","DOCTOR","DOG","DOMAINS","DOT","DOWNLOAD","DRIVE","DTV","DUBAI","DUCK","DUNLOP","DUPONT","DURBAN","DVAG","DVR","DZ","EARTH","EAT","EC","ECO","EDEKA","EDU","EDUCATION","EE","EG","EMAIL","EMERCK","ENERGY","ENGINEER","ENGINEERING","ENTERPRISES","EPSON","EQUIPMENT","ER","ERICSSON","ERNI","ES","ESQ","ESTATE","ESURANCE","ET","ETISALAT","EU","EUROVISION","EUS","EVENTS","EXCHANGE","EXPERT","EXPOSED","EXPRESS","EXTRASPACE","FAGE","FAIL","FAIRWINDS","FAITH","FAMILY","FAN","FANS","FARM","FARMERS","FASHION","FAST","FEDEX","FEEDBACK","FERRARI","FERRERO","FI","FIAT","FIDELITY","FIDO","FILM","FINAL","FINANCE","FINANCIAL","FIRE","FIRESTONE","FIRMDALE","FISH","FISHING","FIT","FITNESS","FJ","FK","FLICKR","FLIGHTS","FLIR","FLORIST","FLOWERS","FLY","FM","FO","FOO","FOOD","FOODNETWORK","FOOTBALL","FORD","FOREX","FORSALE","FORUM","FOUNDATION","FOX","FR","FREE","FRESENIUS","FRL","FROGANS","FRONTDOOR","FRONTIER","FTR","FUJITSU","FUJIXEROX","FUN","FUND","FURNITURE","FUTBOL","FYI","GA","GAL","GALLERY","GALLO","GALLUP","GAME","GAMES","GAP","GARDEN","GAY","GB","GBIZ","GD","GDN","GE","GEA","GENT","GENTING","GEORGE","GF","GG","GGEE","GH","GI","GIFT","GIFTS","GIVES","GIVING","GL","GLADE","GLASS","GLE","GLOBAL","GLOBO","GM","GMAIL","GMBH","GMO","GMX","GN","GODADDY","GOLD","GOLDPOINT","GOLF","GOO","GOODYEAR","GOOG","GOOGLE","GOP","GOT","GOV","GP","GQ","GR","GRAINGER","GRAPHICS","GRATIS","GREEN","GRIPE","GROCERY","GROUP","GS","GT","GU","GUARDIAN","GUCCI","GUGE","GUIDE","GUITARS","GURU","GW","GY","HAIR","HAMBURG","HANGOUT","HAUS","HBO","HDFC","HDFCBANK","HEALTH","HEALTHCARE","HELP","HELSINKI","HERE","HERMES","HGTV","HIPHOP","HISAMITSU","HITACHI","HIV","HK","HKT","HM","HN","HOCKEY","HOLDINGS","HOLIDAY","HOMEDEPOT","HOMEGOODS","HOMES","HOMESENSE","HONDA","HORSE","HOSPITAL","HOST","HOSTING","HOT","HOTELES","HOTELS","HOTMAIL","HOUSE","HOW","HR","HSBC","HT","HU","HUGHES","HYATT","HYUNDAI","IBM","ICBC","ICE","ICU","ID","IE","IEEE","IFM","IKANO","IL","IM","IMAMAT","IMDB","IMMO","IMMOBILIEN","IN","INC","INDUSTRIES","INFINITI","INFO","ING","INK","INSTITUTE","INSURANCE","INSURE","INT","INTEL","INTERNATIONAL","INTUIT","INVESTMENTS","IO","IPIRANGA","IQ","IR","IRISH","IS","ISMAILI","IST","ISTANBUL","IT","ITAU","ITV","IVECO","JAGUAR","JAVA","JCB","JCP","JE","JEEP","JETZT","JEWELRY","JIO","JLL","JM","JMP","JNJ","JO","JOBS","JOBURG","JOT","JOY","JP","JPMORGAN","JPRS","JUEGOS","JUNIPER","KAUFEN","KDDI","KE","KERRYHOTELS","KERRYLOGISTICS","KERRYPROPERTIES","KFH","KG","KH","KI","KIA","KIM","KINDER","KINDLE","KITCHEN","KIWI","KM","KN","KOELN","KOMATSU","KOSHER","KP","KPMG","KPN","KR","KRD","KRED","KUOKGROUP","KW","KY","KYOTO","KZ","LA","LACAIXA","LAMBORGHINI","LAMER","LANCASTER","LANCIA","LAND","LANDROVER","LANXESS","LASALLE","LAT","LATINO","LATROBE","LAW","LAWYER","LB","LC","LDS","LEASE","LECLERC","LEFRAK","LEGAL","LEGO","LEXUS","LGBT","LI","LIDL","LIFE","LIFEINSURANCE","LIFESTYLE","LIGHTING","LIKE","LILLY","LIMITED","LIMO","LINCOLN","LINDE","LINK","LIPSY","LIVE","LIVING","LIXIL","LK","LLC","LLP","LOAN","LOANS","LOCKER","LOCUS","LOFT","LOL","LONDON","LOTTE","LOTTO","LOVE","LPL","LPLFINANCIAL","LR","LS","LT","LTD","LTDA","LU","LUNDBECK","LUPIN","LUXE","LUXURY","LV","LY","MA","MACYS","MADRID","MAIF","MAISON","MAKEUP","MAN","MANAGEMENT","MANGO","MAP","MARKET","MARKETING","MARKETS","MARRIOTT","MARSHALLS","MASERATI","MATTEL","MBA","MC","MCKINSEY","MD","ME","MED","MEDIA","MEET","MELBOURNE","MEME","MEMORIAL","MEN","MENU","MERCKMSD","METLIFE","MG","MH","MIAMI","MICROSOFT","MIL","MINI","MINT","MIT","MITSUBISHI","MK","ML","MLB","MLS","MM","MMA","MN","MO","MOBI","MOBILE","MODA","MOE","MOI","MOM","MONASH","MONEY","MONSTER","MORMON","MORTGAGE","MOSCOW","MOTO","MOTORCYCLES","MOV","MOVIE","MP","MQ","MR","MS","MSD","MT","MTN","MTR","MU","MUSEUM","MUTUAL","MV","MW","MX","MY","MZ","NA","NAB","NADEX","NAGOYA","NAME","NATIONWIDE","NATURA","NAVY","NBA","NC","NE","NEC","NET","NETBANK","NETFLIX","NETWORK","NEUSTAR","NEW","NEWHOLLAND","NEWS","NEXT","NEXTDIRECT","NEXUS","NF","NFL","NG","NGO","NHK","NI","NICO","NIKE","NIKON","NINJA","NISSAN","NISSAY","NL","NO","NOKIA","NORTHWESTERNMUTUAL","NORTON","NOW","NOWRUZ","NOWTV","NP","NR","NRA","NRW","NTT","NU","NYC","NZ","OBI","OBSERVER","OFF","OFFICE","OKINAWA","OLAYAN","OLAYANGROUP","OLDNAVY","OLLO","OM","OMEGA","ONE","ONG","ONL","ONLINE","ONYOURSIDE","OOO","OPEN","ORACLE","ORANGE","ORG","ORGANIC","ORIGINS","OSAKA","OTSUKA","OTT","OVH","PA","PAGE","PANASONIC","PARIS","PARS","PARTNERS","PARTS","PARTY","PASSAGENS","PAY","PCCW","PE","PET","PF","PFIZER","PG","PH","PHARMACY","PHD","PHILIPS","PHONE","PHOTO","PHOTOGRAPHY","PHOTOS","PHYSIO","PICS","PICTET","PICTURES","PID","PIN","PING","PINK","PIONEER","PIZZA","PK","PL","PLACE","PLAY","PLAYSTATION","PLUMBING","PLUS","PM","PN","PNC","POHL","POKER","POLITIE","PORN","POST","PR","PRAMERICA","PRAXI","PRESS","PRIME","PRO","PROD","PRODUCTIONS","PROF","PROGRESSIVE","PROMO","PROPERTIES","PROPERTY","PROTECTION","PRU","PRUDENTIAL","PS","PT","PUB","PW","PWC","PY","QA","QPON","QUEBEC","QUEST","QVC","RACING","RADIO","RAID","RE","READ","REALESTATE","REALTOR","REALTY","RECIPES","RED","REDSTONE","REDUMBRELLA","REHAB","REISE","REISEN","REIT","RELIANCE","REN","RENT","RENTALS","REPAIR","REPORT","REPUBLICAN","REST","RESTAURANT","REVIEW","REVIEWS","REXROTH","RICH","RICHARDLI","RICOH","RIGHTATHOME","RIL","RIO","RIP","RMIT","RO","ROCHER","ROCKS","RODEO","ROGERS","ROOM","RS","RSVP","RU","RUGBY","RUHR","RUN","RW","RWE","RYUKYU","SA","SAARLAND","SAFE","SAFETY","SAKURA","SALE","SALON","SAMSCLUB","SAMSUNG","SANDVIK","SANDVIKCOROMANT","SANOFI","SAP","SARL","SAS","SAVE","SAXO","SB","SBI","SBS","SC","SCA","SCB","SCHAEFFLER","SCHMIDT","SCHOLARSHIPS","SCHOOL","SCHULE","SCHWARZ","SCIENCE","SCJOHNSON","SCOR","SCOT","SD","SE","SEARCH","SEAT","SECURE","SECURITY","SEEK","SELECT","SENER","SERVICES","SES","SEVEN","SEW","SEX","SEXY","SFR","SG","SH","SHANGRILA","SHARP","SHAW","SHELL","SHIA","SHIKSHA","SHOES","SHOP","SHOPPING","SHOUJI","SHOW","SHOWTIME","SHRIRAM","SI","SILK","SINA","SINGLES","SITE","SJ","SK","SKI","SKIN","SKY","SKYPE","SL","SLING","SM","SMART","SMILE","SN","SNCF","SO","SOCCER","SOCIAL","SOFTBANK","SOFTWARE","SOHU","SOLAR","SOLUTIONS","SONG","SONY","SOY","SPACE","SPORT","SPOT","SPREADBETTING","SR","SRL","SS","ST","STADA","STAPLES","STAR","STATEBANK","STATEFARM","STC","STCGROUP","STOCKHOLM","STORAGE","STORE","STREAM","STUDIO","STUDY","STYLE","SU","SUCKS","SUPPLIES","SUPPLY","SUPPORT","SURF","SURGERY","SUZUKI","SV","SWATCH","SWIFTCOVER","SWISS","SX","SY","SYDNEY","SYMANTEC","SYSTEMS","SZ","TAB","TAIPEI","TALK","TAOBAO","TARGET","TATAMOTORS","TATAR","TATTOO","TAX","TAXI","TC","TCI","TD","TDK","TEAM","TECH","TECHNOLOGY","TEL","TEMASEK","TENNIS","TEVA","TF","TG","TH","THD","THEATER","THEATRE","TIAA","TICKETS","TIENDA","TIFFANY","TIPS","TIRES","TIROL","TJ","TJMAXX","TJX","TK","TKMAXX","TL","TM","TMALL","TN","TO","TODAY","TOKYO","TOOLS","TOP","TORAY","TOSHIBA","TOTAL","TOURS","TOWN","TOYOTA","TOYS","TR","TRADE","TRADING","TRAINING","TRAVEL","TRAVELCHANNEL","TRAVELERS","TRAVELERSINSURANCE","TRUST","TRV","TT","TUBE","TUI","TUNES","TUSHU","TV","TVS","TW","TZ","UA","UBANK","UBS","UG","UK","UNICOM","UNIVERSITY","UNO","UOL","UPS","US","UY","UZ","VA","VACATIONS","VANA","VANGUARD","VC","VE","VEGAS","VENTURES","VERISIGN","VERSICHERUNG","VET","VG","VI","VIAJES","VIDEO","VIG","VIKING","VILLAS","VIN","VIP","VIRGIN","VISA","VISION","VISTAPRINT","VIVA","VIVO","VLAANDEREN","VN","VODKA","VOLKSWAGEN","VOLVO","VOTE","VOTING","VOTO","VOYAGE","VU","VUELOS","WALES","WALMART","WALTER","WANG","WANGGOU","WATCH","WATCHES","WEATHER","WEATHERCHANNEL","WEBCAM","WEBER","WEBSITE","WED","WEDDING","WEIBO","WEIR","WF","WHOSWHO","WIEN","WIKI","WILLIAMHILL","WIN","WINDOWS","WINE","WINNERS","WME","WOLTERSKLUWER","WOODSIDE","WORK","WORKS","WORLD","WOW","WS","WTC","WTF","XBOX","XEROX","XFINITY","XIHUAN","XIN","XN--11B4C3D","XN--1CK2E1B","XN--1QQW23A","XN--2SCRJ9C","XN--30RR7Y","XN--3BST00M","XN--3DS443G","XN--3E0B707E","XN--3HCRJ9C","XN--3OQ18VL8PN36A","XN--3PXU8K","XN--42C2D9A","XN--45BR5CYL","XN--45BRJ9C","XN--45Q11C","XN--4GBRIM","XN--54B7FTA0CC","XN--55QW42G","XN--55QX5D","XN--5SU34J936BGSG","XN--5TZM5G","XN--6FRZ82G","XN--6QQ986B3XL","XN--80ADXHKS","XN--80AO21A","XN--80AQECDR1A","XN--80ASEHDB","XN--80ASWG","XN--8Y0A063A","XN--90A3AC","XN--90AE","XN--90AIS","XN--9DBQ2A","XN--9ET52U","XN--9KRT00A","XN--B4W605FERD","XN--BCK1B9A5DRE4C","XN--C1AVG","XN--C2BR7G","XN--CCK2B3B","XN--CG4BKI","XN--CLCHC0EA0B2G2A9GCD","XN--CZR694B","XN--CZRS0T","XN--CZRU2D","XN--D1ACJ3B","XN--D1ALF","XN--E1A4C","XN--ECKVDTC9D","XN--EFVY88H","XN--ESTV75G","XN--FCT429K","XN--FHBEI","XN--FIQ228C5HS","XN--FIQ64B","XN--FIQS8S","XN--FIQZ9S","XN--FJQ720A","XN--FLW351E","XN--FPCRJ9C3D","XN--FZC2C9E2C","XN--FZYS8D69UVGM","XN--G2XX48C","XN--GCKR3F0F","XN--GECRJ9C","XN--GK3AT1E","XN--H2BREG3EVE","XN--H2BRJ9C","XN--H2BRJ9C8C","XN--HXT814E","XN--I1B6B1A6A2E","XN--IMR513N","XN--IO0A7I","XN--J1AEF","XN--J1AMH","XN--J6W193G","XN--JLQ61U9W7B","XN--JVR189M","XN--KCRX77D1X4A","XN--KPRW13D","XN--KPRY57D","XN--KPU716F","XN--KPUT3I","XN--L1ACC","XN--LGBBAT1AD8J","XN--MGB9AWBF","XN--MGBA3A3EJT","XN--MGBA3A4F16A","XN--MGBA7C0BBN0A","XN--MGBAAKC7DVF","XN--MGBAAM7A8H","XN--MGBAB2BD","XN--MGBAH1A3HJKRD","XN--MGBAI9AZGQP6J","XN--MGBAYH7GPA","XN--MGBBH1A","XN--MGBBH1A71E","XN--MGBC0A9AZCG","XN--MGBCA7DZDO","XN--MGBERP4A5D4AR","XN--MGBGU82A","XN--MGBI4ECEXP","XN--MGBPL2FH","XN--MGBT3DHD","XN--MGBTX2B","XN--MGBX4CD0AB","XN--MIX891F","XN--MK1BU44C","XN--MXTQ1M","XN--NGBC5AZD","XN--NGBE9E0A","XN--NGBRX","XN--NODE","XN--NQV7F","XN--NQV7FS00EMA","XN--NYQY26A","XN--O3CW4H","XN--OGBPF8FL","XN--OTU796D","XN--P1ACF","XN--P1AI","XN--PBT977C","XN--PGBS0DH","XN--PSSY2U","XN--Q9JYB4C","XN--QCKA1PMC","XN--QXA6A","XN--QXAM","XN--RHQV96G","XN--ROVU88B","XN--RVC1E0AM3E","XN--S9BRJ9C","XN--SES554G","XN--T60B56A","XN--TCKWE","XN--TIQ49XQYJ","XN--UNUP4Y","XN--VERMGENSBERATER-CTB","XN--VERMGENSBERATUNG-PWB","XN--VHQUV","XN--VUQ861B","XN--W4R85EL8FHU5DNRA","XN--W4RS40L","XN--WGBH1C","XN--WGBL6A","XN--XHQ521B","XN--XKC2AL3HYE2A","XN--XKC2DL3A5EE0H","XN--Y9A3AQ","XN--YFRO4I67O","XN--YGBI2AMMX","XN--ZFR164B","XXX","XYZ","YACHTS","YAHOO","YAMAXUN","YANDEX","YE","YODOBASHI","YOGA","YOKOHAMA","YOU","YOUTUBE","YT","YUN","ZA","ZAPPOS","ZARA","ZERO","ZIP","ZM","ZONE","ZUERICH","ZW"
]

def process_file(name, f):
    """
    TODO
    This function takes in a filename along with the file object (actually
    a StringIO object at submission time) and
    scans its contents against regex patterns. It returns a list of
    (filename, type, value) tuples where type is either an 'e' or a 'p'
    for e-mail or phone, and value is the formatted phone number or e-mail.
    The canonical formats are:
         (name, 'p', '###-###-#####')
         (name, 'e', 'someone@something')
    If the numbers you submit are formatted differently they will not
    match the gold answers

    NOTE: ***don't change this interface***, as it will be called directly by
    the submit script

    NOTE: You shouldn't need to worry about this, but just so you know, the
    'f' parameter below will be of type StringIO at submission time. So, make
    sure you check the StringIO interface if you do anything really tricky,
    though StringIO should support most everything.
    """
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    teresa = " (followed by \""
    ouster = " (followed by &ldquo;"
    melissa1 = "<em>"
    melissa2 = "</em>"
    change = [" (followed by \""," (followed by &ldquo;"," dot "," dt "," DOM ","<em>","</em>"]
    res = []
    for line in f:
        #Pre processing for ouster file and various dots
        for c in change:
            if c in line:
                new = ""
                if c == teresa or c == ouster or c == melissa1 or c == melissa2:
                    new = line.replace(c, '')
                else:
                    new = line.replace(c, '.')
                line = new

        for e in email_pat:
            matches = re.findall(e, line)
            for m in matches:

                if '-' in m[-1]: #dlwh case
                    temp = []
                    for p in m:
                        temp.append(p.replace('-',''))
                    m = temp
                if ' ' in m[1]:
                    temp = []
                    for p in m:
                        temp.append(p.replace(' ','.'))
                    m = temp      


                if 'obfuscate' in e:
                    email = m[2] + '@' + m[0] + '.' + m[1]
                    res.append((name, 'e', email))
                elif 'server' != m[0].lower() and m[-1].upper() in TLD:
                    email = ""
                    for i,t in enumerate(m):
                        if i == 0:
                            email = t
                        elif i == 1:
                            email += '@' + t
                        else:
                            email += '.' + t
                    email = email.replace(';', '.')
                    email = email.replace('-', '')
                    res.append((name, 'e', email))

        # for e in email_pat2:
        #     matches = re.findall(e, line)
        #     for m in matches:
        #         print("hi")
        #         if 'server' != m[0].lower() and m[-1].upper() in TLD:
        #             email = ""
        #             for i,t in enumerate(m):
        #                 if i == 0:
        #                     email = t
        #                 elif i == 1:
        #                     email += '@' + t
        #                 else:
        #                     email += '.' + t
        #             res.append((name, 'e', email))
        # for e in email_pat2:
        #     matches = re.findall(e, line)
        #     for m in matches:
        #         if 'edu' in e and 'server' != m[0].lower():
        #             email = '%s@%s.%s.edu' %m
        #             res.append((name, 'e', email))
        #             #print("2", email)

        #         elif 'com' in e and 'server' != m[0].lower():
        #             email = '%s@%s.%s.com' % m
        #             res.append((name, 'e', email))
        #             #print("2", email)
        #         elif 'obfuscate' in e:
        #             email = m[2] + '@' + m[0] + '.' + m[1]
        #             res.append((name, 'e', email))

        # for e in email_pat3:
        #     matches = re.findall(e, line)
        #     if 'edu' in e:
        #         for m in matches:
        #             #print(m)
        #             email = '%s.%s@%s.edu' %m
        #             res.append((name, 'e', email))
        #             print("3", email)

        #     elif 'com' in e:
        #         for m in matches:
        #             print(m)
        #             email = '%s.%s@%s.com' % m
        #             res.append((name, 'e', email))
        #             print("3", email)
        
        # for e in email_pat4:
        #     matches = re.findall(e, line)
        #     if 'edu' in e:
        #         for m in matches:
        #             email = '%s.%s@%s.%s.edu' %m
        #             res.append((name, 'e', email))
        #             print("4", email)

        #     elif 'com' in e:
        #         for m in matches:
        #             print(m)
        #             email = '%s.%s@%s.%s.com' % m
        #             res.append((name, 'e', email))
        #             print("4", email)

        for p in phone_pat:
            matches = re.findall(p, line)
            for m in matches:
                phone = '%s-%s-%s' % m  #phone formula
                res.append((name, 'p', phone))
    return res


def process_dir(data_path):
    """
    You should not need to edit this function, nor should you alter
    its interface as it will be called directly by the submit script
    """
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path, fname)
        f = open(path, 'r', encoding='ISO-8859-1')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list


def get_gold(gold_path):
    """
    You should not need to edit this function.
    Given a path to a tsv file of gold e-mails and phone numbers
    this function returns a list of tuples of the canonical form:
    (filename, type, value)
    """
    # get gold answers
    gold_list = []
    f_gold = open(gold_path, 'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list


def score(guess_list, gold_list):
    """
    You should not need to edit this function.
    Given a list of guessed contacts and gold contacts, this function
    computes the intersection and set differences, to compute the true
    positives, false positives and false negatives.  Importantly, it
    converts all of the values to lower case before comparing
    """
    guess_list = [
        (fname, _type, value.lower())
        for (fname, _type, value)
        in guess_list
    ]
    gold_list = [
        (fname, _type, value.lower())
        for (fname, _type, value)
        in gold_list
    ]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    # print('Guesses (%d): ' % len(guess_set))
    # pp.pprint(guess_set)
    # print('Gold (%d): ' % len(gold_set))
    # pp.pprint(gold_set)
    print('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print('Summary: tp=%d, fp=%d, fn=%d' % (len(tp), len(fp), len(fn)))


def main(data_path, gold_path):
    """
    You should not need to edit this function.
    It takes in the string path to the data directory and the
    gold file
    """
    guess_list = process_dir(data_path)
    gold_list = get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print('usage:\tSpamLord.py <data_dir> <gold_file>')
        sys.exit(0)
    main(sys.argv[1], sys.argv[2])
