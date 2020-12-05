# multi patters
R_MULTI = r'(.*)\bvagy\b(.*)|(.*)\bés\b(.*)'

# schemas
R_TOLIG = r'([:\w ]*-?t[oóöő]l)([:\w ]*-?ig)'
R_TOL = r'([:\w ]*-?t[oóöő]l).*'
R_IG = r'([:\w ]*-?ig)'

# hyper day level patterns
R_ISO_DATE = r'\b(\d{1,4})(?:[-\\/\.](1[0-2]|0?[1-9]))?(?:[-\\/\.](1[0-9]|2[0-9]|3[01]|0?[1-9]))?'
R_NAMED_MONTH = r'.*(\bjan(?:\b|\.|u[aá]r){1}|\bfeb(?:\b|r\.|\.|ru[aá]r){1}|\bm[aá]r(?:\b|c\b|c\.|\.|cius){1}|\b[aá]pr(?:\b|\.|ilis){1}\bm[aá]j(?:\b|\.|us){1}|\bj[uú]n(?:\b|\.|ius){1}|\bj[uú]l(?:\b|\.|ius){1}|\baug(?:\b|\.|usztus){1}|\bszep(?:t\b|t\.|\b|\.|tember){1}|\bokt(?:\b|\.|[oó]ber){1}|\bnov(?:\b|\.|ember){1}|\bdec(?:\b|\.|ember){1}) ([1-3][0-9]|[1-9])?'
r_ma = r'(\b(má(?:tól|ra).*)\b|\b(ma .*)\b|\b(mai nap[a-z]*.*)\b)'
r_holnap = r'(holnap(?!után).*)'
r_holnaputan = r'(holnapután.*)'
r_nnap_mulva = r'(([\w]*) nap m[úu]lva)'

# hour level
r_kor = r'([:\w ]*-?kor)'

# hour+minute parsers
r_digi = r'([0-2][0-9]):([0-9][0-9])'
r_words = r'([0-2][0-9])(?: ?óra|-?kor| ?h) ?(?:([0-9][0-9])(?:(?: ?perc| ?p)[\w]*))? ?(?:([0-9][0-9])(?:(?: ?m[áa]sodperc| ?mp)[\w]*))?'