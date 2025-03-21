# multi patters
R_MULTI = r'(.*)\bvagy\b(.*)|(.*)\bés\b(.*)'

# schemas
R_TOLIG = r'(.*-?t[oóöő]l\b|.* [oó]ta\b)(.*-?ig\b)'
R_TOL = r'([:\w ]*-?t[oóöő]l\b|.* [oó]ta\b).*'
R_IG = r'([:\w ]*-?ig\b)'

# tol-ig hyphen separated
R_TOLIG_YMD = r"((?:\b\d{4,4}) ?(?:\bjan(?:\b|\.|u[aá]r){1}|\bfeb(?:\b|r\.|\.|ru[aá]r){1}|\bm[aá]r(?:\b|c\b|c\.|\.|cius){1}|\b[aá]pr(?:\b|\.|ilis){1}\b|m[aá]j(?:\b|\.|us){1}|\bj[uú]n(?:\b|\.|ius){1}|\bj[uú]l(?:\b|\.|ius){1}|\baug(?:\b|\.|usztus){1}|\bszep(?:t\b|t\.|\b|\.|tember){1}|\bokt(?:\b|\.|[oó]ber){1}|\bnov(?:\b|\.|ember){1}|\bdec(?:\b|\.|ember))(?: (?:[1-3][0-9]|[1-9]|egy.{0,5}|kett[őöo].{0,5}|h[aá]rom.{0,5}|n[eée]gy.{0,5}|öt.{0,5}|hat.{0,5}|h[eé]t.{0,5}|nyolc.{0,5}|kilenc.{0,5}|tíz.{0,5}|tizen.{0,10}|huszon.{0,10}|harminc.{0,10}|elsej[eé].{0,5}|második[aá].{0,5}|harmadik[aá].{0,5}|negyedik[eé].{0,5}|ötödik[eé].{0,5}|hatodik[aá].{0,5}|hetedik[eé].{0,5}|nyolcadik[aá].{0,5}|kilencedik[eé].{0,5}|tizedik[eé].{0,5}|tizen.{0,10}|huszadik[aá].{0,5}|huszon.{0,10}|harmincadik[aá].{0,5}))) ?- ?((?:\b\d{4,4})? ?(?:\bjan(?:\b|\.|u[aá]r)|\bfeb(?:\b|r\.|\.|ru[aá]r)|\bm[aá]r(?:\b|c\b|c\.|\.|cius)|\b[aá]pr(?:\b|\.|ilis)|\bm[aá]j(?:\b|\.|us)|\bj[uú]n(?:\b|\.|ius)|\bj[uú]l(?:\b|\.|ius)|\baug(?:\b|\.|usztus)|\bszep(?:t\b|t\.|\b|\.|tember)|\bokt(?:\b|\.|[oó]ber)|\bnov(?:\b|\.|ember)|\bdec(?:\b|\.|ember))(?: (?:[1-3][0-9]|[1-9]|egy.{0,5}|kett[őöo].{0,5}|h[aá]rom.{0,5}|n[eée]gy.{0,5}|öt.{0,5}|hat.{0,5}|h[eé]t.{0,5}|nyolc.{0,5}|kilenc.{0,5}|tíz.{0,5}|tizen.{0,10}|huszon.{0,10}|harminc.{0,10}|elsej[eé].{0,5}|második[aá].{0,5}|harmadik[aá].{0,5}|negyedik[eé].{0,5}|ötödik[eé].{0,5}|hatodik[aá].{0,5}|hetedik[eé].{0,5}|nyolcadik[aá].{0,5}|kilencedik[eé].{0,5}|tizedik[eé].{0,5}|tizen.{0,10}|huszadik[aá].{0,5}|huszon.{0,10}|harmincadik[aá].{0,5})))"
R_TOLIG_MD = r"((?:\bjan(?:\b|\.|u[aá]r){1}|\bfeb(?:\b|r\.|\.|ru[aá]r){1}|\bm[aá]r(?:\b|c\b|c\.|\.|cius){1}|\b[aá]pr(?:\b|\.|ilis){1}\b|m[aá]j(?:\b|\.|us){1}|\bj[uú]n(?:\b|\.|ius){1}|\bj[uú]l(?:\b|\.|ius){1}|\baug(?:\b|\.|usztus){1}|\bszep(?:t\b|t\.|\b|\.|tember){1}|\bokt(?:\b|\.|[oó]ber){1}|\bnov(?:\b|\.|ember){1}|\bdec(?:\b|\.|ember))(?: (?:[1-3][0-9]|[1-9]|egy.{0,5}|kett[őöo].{0,5}|h[aá]rom.{0,5}|n[eée]gy.{0,5}|öt.{0,5}|hat.{0,5}|h[eé]t.{0,5}|nyolc.{0,5}|kilenc.{0,5}|tíz.{0,5}|tizen.{0,10}|huszon.{0,10}|harminc.{0,10}|elsej[eé].{0,5}|második[aá].{0,5}|harmadik[aá].{0,5}|negyedik[eé].{0,5}|ötödik[eé].{0,5}|hatodik[aá].{0,5}|hetedik[eé].{0,5}|nyolcadik[aá].{0,5}|kilencedik[eé].{0,5}|tizedik[eé].{0,5}|tizen.{0,10}|huszadik[aá].{0,5}|huszon.{0,10}|harmincadik[aá].{0,5}))) ?-( ?(?:\bjan(?:\b|\.|u[aá]r)|\bfeb(?:\b|r\.|\.|ru[aá]r)|\bm[aá]r(?:\b|c\b|c\.|\.|cius)|\b[aá]pr(?:\b|\.|ilis)|\bm[aá]j(?:\b|\.|us)|\bj[uú]n(?:\b|\.|ius)|\bj[uú]l(?:\b|\.|ius)|\baug(?:\b|\.|usztus)|\bszep(?:t\b|t\.|\b|\.|tember)|\bokt(?:\b|\.|[oó]ber)|\bnov(?:\b|\.|ember)|\bdec(?:\b|\.|ember))(?: (?:[1-3][0-9]|[1-9]|egy.{0,5}|kett[őöo].{0,5}|h[aá]rom.{0,5}|n[eée]gy.{0,5}|öt.{0,5}|hat.{0,5}|h[eé]t.{0,5}|nyolc.{0,5}|kilenc.{0,5}|tíz.{0,5}|tizen.{0,10}|huszon.{0,10}|harminc.{0,10}|elsej[eé].{0,5}|második[aá].{0,5}|harmadik[aá].{0,5}|negyedik[eé].{0,5}|ötödik[eé].{0,5}|hatodik[aá].{0,5}|hetedik[eé].{0,5}|nyolcadik[aá].{0,5}|kilencedik[eé].{0,5}|tizedik[eé].{0,5}|tizen.{0,10}|huszadik[aá].{0,5}|huszon.{0,10}|harmincadik[aá].{0,5})))"
R_TOLIG_YM = r"((?:\b\d{4,4}) ?(?:\bjan(?:\b|\.|u[aá]r){1}|\bfeb(?:\b|r\.|\.|ru[aá]r){1}|\bm[aá]r(?:\b|c\b|c\.|\.|cius){1}|\b[aá]pr(?:\b|\.|ilis){1}\b|m[aá]j(?:\b|\.|us){1}|\bj[uú]n(?:\b|\.|ius){1}|\bj[uú]l(?:\b|\.|ius){1}|\baug(?:\b|\.|usztus){1}|\bszep(?:t\b|t\.|\b|\.|tember){1}|\bokt(?:\b|\.|[oó]ber){1}|\bnov(?:\b|\.|ember){1}|\bdec(?:\b|\.|ember))) ?- ?((?:\b\d{4,4})? ?(?:\bjan(?:\b|\.|u[aá]r)|\bfeb(?:\b|r\.|\.|ru[aá]r)|\bm[aá]r(?:\b|c\b|c\.|\.|cius)|\b[aá]pr(?:\b|\.|ilis)|\bm[aá]j(?:\b|\.|us)|\bj[uú]n(?:\b|\.|ius)|\bj[uú]l(?:\b|\.|ius)|\baug(?:\b|\.|usztus)|\bszep(?:t\b|t\.|\b|\.|tember)|\bokt(?:\b|\.|[oó]ber)|\bnov(?:\b|\.|ember)|\bdec(?:\b|\.|ember)))"
R_TOLIG_M = r"((?:\bjan(?:\b|\.|u[aá]r){1}|\bfeb(?:\b|r\.|\.|ru[aá]r){1}|\bm[aá]r(?:\b|c\b|c\.|\.|cius){1}|\b[aá]pr(?:\b|\.|ilis){1}\b|m[aá]j(?:\b|\.|us){1}|\bj[uú]n(?:\b|\.|ius){1}|\bj[uú]l(?:\b|\.|ius){1}|\baug(?:\b|\.|usztus){1}|\bszep(?:t\b|t\.|\b|\.|tember){1}|\bokt(?:\b|\.|[oó]ber){1}|\bnov(?:\b|\.|ember){1}|\bdec(?:\b|\.|ember))) ?-( ?(?:\bjan(?:\b|\.|u[aá]r)|\bfeb(?:\b|r\.|\.|ru[aá]r)|\bm[aá]r(?:\b|c\b|c\.|\.|cius)|\b[aá]pr(?:\b|\.|ilis)|\bm[aá]j(?:\b|\.|us)|\bj[uú]n(?:\b|\.|ius)|\bj[uú]l(?:\b|\.|ius)|\baug(?:\b|\.|usztus)|\bszep(?:t\b|t\.|\b|\.|tember)|\bokt(?:\b|\.|[oó]ber)|\bnov(?:\b|\.|ember)|\bdec(?:\b|\.|ember)))"
R_TOLIG_Y = r"(\b\d{4,4}) ?- ?(\b\d{4,4})"

# hyper day level patterns
R_ISO_DATE = r'(\b\d{4,4})(?:[-\\/\. ] ?(1[0-2]|0?[1-9]))?(?:[-\\/\. ] ?(1[0-9]|2[0-9]|3[01]|0?[1-9]))?'
R_REV_ISO_DATE = r'\b(1[0-9]|2[0-9]|3[01]|0?[1-9])[-\\/\. ] ?(1[0-2]|0?[1-9])[-\\/\. ] ?(\b\d{4,4})'
R_NAMED_MONTH = r'\b(j[oöő]v[oöő].*?|tavaly.*?)?(\bjan(?:\b|\.|u[aá]r){1}|\bfeb(?:\b|r\.|\.|ru[aá]r){1}|\bm[aá]r(?:\b|c\b|c\.|\.|cius){1}|\b[aá]pr(?:\b|\.|ilis){1}\b|m[aá]j(?:\b|\.|us){1}|\bj[uú]n(?:\b|\.|ius){1}|\bj[uú]l(?:\b|\.|ius){1}|\baug(?:\b|\.|usztus){1}|\bszep(?:t\b|t\.|\b|\.|tember){1}|\bokt(?:\b|\.|[oó]ber){1}|\bnov(?:\b|\.|ember){1}|\bdec(?:\b|\.|ember))(?: ([1-3][0-9]|[1-9]|egy.{0,5}|kett[őöo].{0,5}|h[aá]rom.{0,5}|n[eée]gy.{0,5}|öt.{0,5}|hat.{0,5}|h[eé]t.{0,5}|nyolc.{0,5}|kilenc.{0,5}|tíz.{0,5}|tizen.{0,10}|huszon.{0,10}|harminc.{0,10}|elsej[eé].{0,5}|második[aá].{0,5}|harmadik[aá].{0,5}|negyedik[eé].{0,5}|ötödik[eé].{0,5}|hatodik[aá].{0,5}|hetedik[eé].{0,5}|nyolcadik[aá].{0,5}|kilencedik[eé].{0,5}|tizedik[eé].{0,5}|tizen.{0,10}|huszadik[aá].{0,5}|huszon.{0,10}|harmincadik[aá].{0,5}))?'
R_RELATIVE_MONTH = r'(?:(\blegut[oó]bbi|\butols[oó]|\bmúlt|\but[oó]bbi|\bezen|\bebben|\baktu[aá]lis|\bj[oöő]v[oöő]|\bk[oö]vetkez[oőö]|\bk[oö]vetkezend[oőö]).*)? a?h[oó]nap'
R_NAMED_MONTH_SME = r"(\b\d{4,4}|j[oöő]v[oöő].*?|tavaly.*?)? ?(\bjan(?:\b|\.|u[aá]r){1}|\bfeb(?:\b|r\.|\.|ru[aá]r){1}|\bm[aá]r(?:\b|c\b|c\.|\.|cius){1}|\b[aá]pr(?:\b|\.|ilis){1}\b|m[aá]j(?:\b|\.|us){1}|\bj[uú]n(?:\b|\.|ius){1}|\bj[uú]l(?:\b|\.|ius){1}|\baug(?:\b|\.|usztus){1}|\bszep(?:t\b|t\.|\b|\.|tember){1}|\bokt(?:\b|\.|[oó]ber){1}|\bnov(?:\b|\.|ember){1}|\bdec(?:\b|\.|ember)) (elej|k[oö]zep|v[eé]g)"

R_WEEKDAY = r'(?:(el[oő]z[oő]|m[uú]lt|ezen|j[oöő]v[oöő]).*)?(h[eé]tf[oő]|kedd|szerd[aá]|cs[uü]t[oö]rt[oö]k|p[eé]ntek|szombat|vas[aá]rnap)'
R_WEEK = r'(el[oő]z[oő] h[eé]t|m[uú]lt h[eé]t|m[uú]lth[eé]t|ezen a? h[eé]t|j[oöő]v[oöő]h[eé]t|j[oöő]v[oöő] h[eé]t)'

R_TODAY = r'\b(má(?:tól|ra))\b|\b(ma)\b|\b(mai nap)\b'
R_TOMORROW = r'\b(holnap)(?!ut[aá]n)'
R_NTOMORROW = r'\b(holnaput[aá]n)'
R_YESTERDAY = r'\b(tegnap)'
R_NYESTERDAY = r'\b(tegnapel[oő]tt)'

R_NMINS_FROM_NOW = r'(([\w]*) perc m[úu]lva)'
R_NHOURS_FROM_NOW = r'(([\w]*) [oó]ra m[úu]lva)'
R_NDAYS_FROM_NOW = r'(([\w]*) nap m[úu]lva)'
R_NWEEKS_FROM_NOW = r'(([\w]*) h[eé]t m[úu]lva)'

R_NMINS_PRIOR_NOW = r'(([\w]*) percc?el (ezel[oöő]tt|kor[aá]bban|kor[aá]bbi))'
R_NHOURS_PRIOR_NOW = r'(([\w]*) [oó]r[aá]val (ezel[oöő]tt|kor[aá]bban|kor[aá]bbi))'
R_NDAYS_PRIOR_NOW = r'(([\w]*) napp?al (ezel[oöő]tt|kor[aá]bban|kor[aá]bbi))'
R_NWEEKS_PRIOR_NOW = r'(([\w]*) h[eé]tt?el (ezel[oöő]tt|kor[aá]bban|kor[aá]bbi))'

R_IN_PAST_PERIOD_MINS = r'(elm[úu]lt|megel[oőö]z[oőö]|el[oőö]z[oőö])\b([ \w]*)\b(percben|perc)'
R_IN_PAST_PERIOD_HOURS = r'(elm[úu]lt|megel[oőö]z[oőö]|el[oőö]z[oőö])\b([ \w]*)\b([oó]r[aá]ban|[oó]rai|[oó]ra)'
R_IN_PAST_PERIOD_DAYS = r'(elm[úu]lt|megel[oőö]z[oőö]|el[oőö]z[oőö])\b([ \w]*)\b(napban|napi|nap)'
R_IN_PAST_PERIOD_WEEKS = r'(elm[úu]lt|megel[oőö]z[oőö]|el[oőö]z[oőö])\b([ \w]*)\b(h[eé]tben|heti|h[eé]t)'
R_IN_PAST_PERIOD_MONTHS = r'(elm[úu]lt|megel[oőö]z[oőö]|el[oőö]z[oőö])\b([ \w]*)\b(h[oó]napban|havi|h[oó]nap)'
R_IN_PAST_PERIOD_YEARS = r'(elm[úu]lt|megel[oőö]z[oőö]|el[oőö]z[oőö])\b([ \w]*)\b([eé]v|[eé]vben|[eé]vi)'

R_YEAR = r'(tavalyel[oöő]tt|id[eé]n|idei|ebben az [eé]vben|j[oöő]v[oöő]re|tavaly|.*[eé]v m[uú]lva|.*[eé]vvel ezel[oő]tt|.*[eé]vvel kor[aá]bban)'

# hour level
R_AT = r'([:\w ]*-?kor)'

# hour+minute parsers
R_DIGI = r'\b([0-2]?[0-9]):([0-9][0-9])'
R_HWORDS = r'([0-2][0-9])(?: ?óra|-?kor| ?h) ?(?:([0-9][0-9])(?:(?: ?perc| ?p)[\w]*))? ?(?:([0-9][0-9])(?:(?: ?m[áa]sodperc| ?mp)[\w]*))?'
R_HWORDS_ = r'([1-2]?[0-9])?h\b'
R_HOUR_MIN = r'(?:(.*hajnal[i]?|.*reggel|.*d[eé]lel[oőö]tt|.*d[eé]lut[aá]n|.*este|.*[eé]jjel))? ?(?:(.*negyed|.*f[eé]l|.*h[aá]romnegyed))? ?(?:(?:\b([0-9]{1,2}|nulla|egy|kett[oöő]|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|kilenc|t[ií]z|tizenegy|tizenkett[oő]|tizenh[aá]rom|tizenn[eé]gy|tizen[oö]t|tizenhat|tizenh[eé]t|tizennyolc|tizenkilenc|h[uú]sz|huszonegy|huszonkett[oöő]|huszonh[aá]rom)(?! [eé]v|perc)-?(?:kor|ra|\b)(?: [oó]ra)?)?((?:el[oő]tt|ut[aá]n)?.*perc)?)?'
R_HOUR_MIN_REV = r'(?:(.*)(?:perc.{0,4}))?? (?:(hajnal[i]?|reggel|d[eé]lel[oőö]tt|d[eé]lut[aá]n|este|[eé]jjel))? ?(negyed|f[eé]l|h[aá]romnegyed)? ?(?:([0-9]{1,2}|nulla|egy|kett[oöő]|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|kilenc|t[ií]z|tizenegy|tizenkett[oő]|tizenh[aá]rom|tizenn[eé]gy|tizen[oö]t|tizenhat|tizenh[eé]t|tizennyolc|tizenkilenc|h[uú]sz|huszonegy|huszonkett[oöő]|huszonh[aá]rom)(?! [eé]v|perc)-?(?:kor|ra|\b)(?: [oó]ra)?)? ?(ut[aá]n|el[oöő]tt)?'

# R_MIN = r'(.*)(?:perc)'
# R_SEC = r'(.*)(?: ?m[áa]sodperc| ?mp)'

# Duration patterns
R_TOL_NAPRA = r"(.*-?t[oóöő]l\b|.*kezd|.*indul)(.*napra|.*napig|.*napos|.*h[eé]tre|.*h[eé]tig|.*hetes\b)"
R_NAPRA_TOL = r"(.*napra|.*napig|.*napos|.*h[eé]tre|.*h[eé]tig|.*hetes\b)(.*-?t[oóöő]l\b|.*kezd|.*indul)"

# Util patterns
R_N_WEEKS = r"\b([ \w]*)\bh[eé]t"
R_N_DAYS = r"(\b\w+)\b(?=\s+nap)"

# tol-ig dates, ie.: március 20-tol 22-ig
R_TOLIG_IMPLIED_END = r"(\bjan(?:uár)?|feb(?:ruár)?|márc(?:ius)?|ápr(?:ilis)?|máj(?:us)?|jún(?:ius)?|júl(?:ius)?|aug(?:usztus)?|szept(?:ember)?|okt(?:óber)?|nov(?:ember)?|dec(?:ember)?)\s?(\d+)-t[oóöő]l\s?(\d+)-ig"

# kezdo: X ...: Y
R_START_STATED_END_IMPLIED = r"(?:[kK]ezd|[iI]ndul).{1,20}:\s*([^:]{1,50}?)\s*:\s*([^:]{1,50})$"

# Duration
R_HOUR_MIN_D = r'.*?(?:([0-9]{1,2}|nulla|egy|kett[oöő]|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|kilenc|t[ií]z|tizenegy|tizenkett[oő]|tizenh[aá]rom|tizenn[eé]gy|tizen[oö]t|tizenhat|tizenh[eé]t|tizennyolc|tizenkilenc|h[uú]sz|huszonegy|huszonkett[oöő]|huszonkettő|huszonhárom) [óo]ra)? ?([a-zA-Z0-9]{1,15}) perc'
R_SPECIAL_HOUR_D = r'.*?(negyed|h[aá]romnegyed|m[aá]sf[eé]l)(?:[oó]r[aá](?:[tr]?[aá]?)).*'  # e.g. negyedóra, másfélórát, másfélórára
R_HOUR_D = r'.*?(?:([0-9]{1,2}|nulla|egy|kett[oöő]|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|kilenc|t[ií]z|tizenegy|tizenkett[oő]|tizenh[aá]rom|tizenn[eé]gy|tizen[oö]t|tizenhat|tizenh[eé]t|tizennyolc|tizenkilenc|h[uú]sz|huszonegy|huszonkett[oöő]|huszonkettő|huszonhárom|[0-9],5)) ?[óo]r[aá]?'
R_HOUR_HOUR_D = r'.*?(?:([0-9]{1,2}|egy|kett[oöő]|h[aá]rom|n[eé]gy|[öo]t|hat|h[eé]t|nyolc|kilenc|t[ií]z)?(?: [eé]s )? ?(h[aá]romnegyed|negyed|f[eé]l|m[aá]sf[eé]l) ?[oó]r[aá])'
