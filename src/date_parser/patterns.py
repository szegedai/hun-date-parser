# multi patters
R_MULTI = r'(.*)\bvagy\b(.*)|(.*)\bés\b(.*)'

# schemas
R_TOLIG = r'(.*-?t[oóöő]l)(.*-?ig)'
R_TOL = r'([:\w ]*-?t[oóöő]l).*'
R_IG = r'([:\w ]*-?ig)'

# hyper day level patterns
R_ISO_DATE = r'(\b\d{1,4})(?:[-\\/\.](1[0-2]|0?[1-9]))?(?:[-\\/\.](1[0-9]|2[0-9]|3[01]|0?[1-9]))?'
R_NAMED_MONTH = r'(\bjan(?:\b|\.|u[aá]r){1}|\bfeb(?:\b|r\.|\.|ru[aá]r){1}|\bm[aá]r(?:\b|c\b|c\.|\.|cius){1}|\b[aá]pr(?:\b|\.|ilis){1}\bm[aá]j(?:\b|\.|us){1}|\bj[uú]n(?:\b|\.|ius){1}|\bj[uú]l(?:\b|\.|ius){1}|\baug(?:\b|\.|usztus){1}|\bszep(?:t\b|t\.|\b|\.|tember){1}|\bokt(?:\b|\.|[oó]ber){1}|\bnov(?:\b|\.|ember){1}|\bdec(?:\b|\.|ember){1})(?: ([1-3][0-9]|[1-9]))?'

R_WEEKDAY = r'(?:(el[oő]z[oő]|m[uú]lt|ezen|j[oöő]v[oöő]).*)?(h[eé]tf[oő]|kedd|szerd[aá]|cs[uü]t[oö]rt[oö]k[oö]n|p[eé]ntek|szombat|vas[aá]rnap)'
R_WEEK = r'(el[oő]z[oő] h[eé]t|m[uú]lt h[eé]t|m[uú]lth[eé]t|ezen a? h[eé]t|j[oöő]v[oöő]h[eé]t|j[oöő]v[oöő] h[eé]t)'

R_TODAY = r'\b(má(?:tól|ra))\b|\b(ma)\b|\b(mai nap)\b'
R_TOMORROW = r'\b(holnap)(?!ut[aá]n)'
R_NTOMORROW = r'\b(holnaput[aá]n)'
R_YESTERDAY = r'\b(tegnap)'
R_NYESTERDAY = r'\b(tegnapel[oő]tt)'
R_NDAYS_FROM_NOW = r'(([\w]*) nap m[úu]lva)'

# hour level
R_AT = r'([:\w ]*-?kor)'

# hour+minute parsers
R_DIGI = r'\b([0-2]?[0-9]):([0-9][0-9])'
R_HWORDS = r'([0-2][0-9])(?: ?óra|-?kor| ?h) ?(?:([0-9][0-9])(?:(?: ?perc| ?p)[\w]*))? ?(?:([0-9][0-9])(?:(?: ?m[áa]sodperc| ?mp)[\w]*))?'