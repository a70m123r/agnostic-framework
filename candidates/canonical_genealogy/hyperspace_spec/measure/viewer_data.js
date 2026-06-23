const SUBSTRATE = {
 "source": "substrate_probe_broad_run.jsonl",
 "n_records": 240,
 "n_parsed": 240,
 "artefacts": [
  {
   "id": "A1",
   "title": "movable-type printing (the technology/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Bi Sheng, Johannes Gutenberg, and later refiners",
     "agreement": 0.188,
     "sharpness": 0.152,
     "measured_frac": 0.688,
     "perBloc": {
      "US": [
       "A diffused network of artisans, scholars, entrepreneurs, and institutions evolving across cultures and centuries.",
       "The diverse agents of its creation, refinement, and dissemination across global cultures and eras.",
       "Johannes Gutenberg, printers, scholars, publishers"
      ],
      "CN": [
       "Jiao Yun (China), Bi Sheng (China), Koreans, Gutenberg (Germany) across East Asian/European transmission",
       "Chinese, Korean, and European innovators (Bi Sheng, Gutenberg, Choe Yun-ui, and printers)",
       "A network of inventors, artisans, merchants, and state actors from East Asia to Europe"
      ],
      "EU": [
       "Bi Sheng, Johannes Gutenberg, and later refiners",
       "Bi Sheng (originator, Song China), Johannes Gutenberg (refiner, Europe), Korean artisans (earlier independent developers), European printers (transmitters and users), colonial printers (global spread)",
       "Bi Sheng (originator, Song Dynasty), Johannes Gutenberg (refiner, Europe), Korean artisans (early adopters/transmitters), European printers (mass adopters), colonial missionaries (global transmitters)"
      ]
     },
     "fan": [
      {
       "reading": "Movable type was independently invented in East Asia and Europe without contact",
       "weight": 0.95,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Evidence of technological transfer via trade routes or diffusion of papermaking",
       "followup": "Study of historical trade networks and comparative technology analysis"
      },
      {
       "reading": "Medieval monks",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Proof of earlier mechanical printing",
       "followup": "Analyze illuminated manuscripts for printing clues"
      },
      {
       "reading": "The cumulative effort of multiple cultures including Chinese artisans (Bi Sheng), Korean metal typographers, and Europea",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Evidence that movalbe type only arose from a single, isolated invention without significant precursor or derivative work.",
       "followup": "Detailed historical tracing of technological transfers and independent innovations in setting and casting type across different civilizations."
      },
      {
       "reading": "Independent development in Korea and China with cross-cultural transmission",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "EU",
       "falsifier": "Lack of material or documentary evidence linking Korean and Chinese type",
       "followup": "Comparative analysis of Korean and Chinese type materials and techniques"
      },
      {
       "reading": "Johannes Gutenberg and his immediate European successors, pivotal for large-scale industrial adoption.",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Historical accounts showing comparable or greater impact from earlier East Asian movable type systems that persisted for centuries.",
       "followup": "Comparative economic and literacy impact studies of printing technologies in Europe and East Asia from the 11th to 17th centuries."
      },
      {
       "reading": "Asian woodblock printers",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence of European prior art",
       "followup": "Investigate early European printing history"
      }
     ]
    },
    "what": {
     "leading": "modular metal type for mass text reproduction",
     "agreement": 0.188,
     "sharpness": 0.188,
     "measured_frac": 1.0,
     "perBloc": {
      "US": [
       "A printing system using reusable, individual characters (type) assembled into pages, inked, and pressed onto a substrate, enabling mass textual replication.",
       "A system of reusable individual characters (types) arranged to form text, inked, and imprinted onto a substrate, enabling mass reproduction of written content.",
       "mechanical printing technology with movable type"
      ],
      "CN": [
       "modular metal type for mass text reproduction",
       "A printing system using individual, reusable type pieces (clay, metal, or wood) to compose text for reproduction",
       "A system for mass-producing text by arranging reusable, individual characters"
      ],
      "EU": [
       "A system of movable metal type for printing",
       "A printing system using reusable metal type pieces",
       "Reusable, modular printing system using individual movable components (e.g., ceramic, wood, metal) to assemble text for mass reproduction"
      ]
     },
     "fan": [
      {
       "reading": "Movable type as a socio-technical system (type + press + ink + paper + labor organization), not just the type itself",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of movable type used without presses or standardized ink/paper",
       "followup": "Study of early printing workshops’ toolkits and labor records"
      },
      {
       "reading": "Movable type includes both the type and the mechanical press as a unified system",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Early Chinese movable type did not use a press, yet is still considered movable type",
       "followup": "Compare technical specifications of Chinese and European printing"
      },
      {
       "reading": "wooden press with movable type",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Discovery of different materials used",
       "followup": "Examine artifacts and historical texts for variations"
      },
      {
       "reading": "A catalyst for the Reformation",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "No correlation between print volume and Reformation spread",
       "followup": "Examine the distribution of religious texts and accompanying movements"
      },
      {
       "reading": "just a set of metal types",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Finding records of usage without supporting press",
       "followup": "Research on early single-use type applications"
      },
      {
       "reading": "Primarily a means of mass communication",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence of it predominantly for specialized artistic use",
       "followup": "Analyze early printed works for purpose and audience"
      }
     ]
    },
    "where": {
     "leading": "Originated in East Asia (China, Korea), later independently developed and widely disseminated across Europe and globally.",
     "agreement": 0.375,
     "sharpness": 0.361,
     "measured_frac": 0.938,
     "perBloc": {
      "US": [
       "Originated in East Asia (China, Korea), later independently developed and widely disseminated across Europe and globally.",
       "Originated in East Asia (China, Korea), diffused globally through trade, empire, and scholarly networks, with major hubs in Europe and later worldwide.",
       "Europe, Asia"
      ],
      "CN": [
       "East Asia (China/Korea), spread via Silk Road to Europe, global",
       "Originated in East Asia (China, Korea), later independently in Europe (Mainz), then spread globally",
       "Originating in East Asia and later independently in Mainz, Germany, spreading globally"
      ],
      "EU": [
       "Originated in China (11th century), spread to Europe (15th century)",
       "Originated in Song China (11th century), independently developed in Goryeo Korea (13th century), refined in Europe (15th century), spread globally via colonialism and trade (16th–19th centuries)",
       "Originated in China (Song Dynasty, 11th c.), refined in Korea (Goryeo Dynasty, 13th–14th c.), revolutionized in Europe (15th c.), spread globally via colonialism (16th–19th c.)"
      ]
     },
     "fan": [
      {
       "reading": "Originated independently in East Asia and Europe, no diffusion",
       "weight": 0.8,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Any shared technological features or intermediaries that indicate transfer",
       "followup": "Genetic analysis of type designs and chemical analysis of inks"
      },
      {
       "reading": "Diffusion solely from Gutenberg's Mainz outward",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Discovery of a contemporaneous, independent printing center elsewhere",
       "followup": "Systematic dating of incunabula to map diffusion patterns"
      },
      {
       "reading": "Originated in Germany, spread to France and England",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Evidence of preexisting printing technologies elsewhere",
       "followup": "Historical documentation of pre-Gutenberg prints"
      },
      {
       "reading": "Global spread via Islamic world (e.g., Ottoman Empire) before European colonialism",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of Islamic movable-type artefacts or texts pre-16th c.",
       "followup": "Review of Ottoman archives for printing records"
      },
      {
       "reading": "Only within the Holy Roman Empire",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Records of prints in non-imperial locations",
       "followup": "Investigate early printing in neighboring regions"
      },
      {
       "reading": "Europe as primary locus of innovation, with Asian contributions marginal",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of Asian movable-type techniques influencing Gutenberg’s work",
       "followup": "Analysis of Gutenberg’s tools/materials for Asian technical traces"
      }
     ]
    },
    "when": {
     "leading": "15th century onwards",
     "agreement": 0.375,
     "sharpness": 0.361,
     "measured_frac": 0.938,
     "perBloc": {
      "US": [
       "15th century onwards",
       "Spanning from its earliest documented use in China (c. 1040 CE), development in Korea (c. 1377 CE), to widespread adoption in Europe from the mid-15th century onward, continuing as a foundational technology.",
       "From approximately the 11th century to the present, with transformative impact from the 15th century onwards."
      ],
      "CN": [
       "11th c. (China) → 13th c. (Korea) → 1440s (Europe) → present",
       "Mid-11th century (Bi Sheng) to present, with key developments in 13th century (Korea) and mid-15th century (Gutenberg)",
       "From 11th-century China through the European explosion c. 1450 to the digital age"
      ],
      "EU": [
       "11th century (China) to present, with key developments in 15th century (Europe)",
       "Temporal extent: 11th century (China) to present (legacy systems); key moments: 1040s (Bi Sheng, China), 1230s (Korea), 1450s (Gutenberg, Europe), 16th–18th centuries (global spread)",
       "11th c. (China, Bi Sheng’s clay type) to 20th c. (decline with offset/digital printing), key moments: 1377 (Korean Jikji, metal type), 1450s (Gutenberg’s press), 16th c. (global spread)"
      ]
     },
     "fan": [
      {
       "reading": "Movable type originated with Bi Sheng in China in 1040, later independently in Korea and Europe",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Proof of direct diffusion from China to Europe, contradicting independence",
       "followup": "Compare type materials, casting methods, and printing press designs"
      },
      {
       "reading": "Independent European invention",
       "weight": 0.7,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Proof of knowledge transfer from East Asia before 1440",
       "followup": "Analyze merchant/missionary records for technical descriptions"
      },
      {
       "reading": "First use circa 1440, transformative impact through the Renaissance",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Identification of earlier uses and impacts",
       "followup": "Examine artifacts dated earlier than 1440"
      },
      {
       "reading": "Continuous development into modern type technologies",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence suggesting printing technology stagnation post-18th century",
       "followup": "Catalog historical advancements and the diffusion of printing methods"
      },
      {
       "reading": "Decline began in 19th c. with industrial presses, not 20th c. digital",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of widespread movable-type use post-1900",
       "followup": "Review of 20th c. printing industry records"
      },
      {
       "reading": "Culminated in modern digital printing technologies",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Proves digital methods negate early significance",
       "followup": "Research on comparative impact of digital vs. movable type"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "mass literacy and standardized language",
     "Increased literacy rates",
     "Widespread literacy and knowledge dissemination",
     "Massive acceleration and democratization of knowledge dissemination, fueling the Renaissan",
     "Creation of new industries and professions (printers, publishers, booksellers) transformin"
    ],
    "aims_by_bloc": {
     "US": [
      "To efficiently reproduce religious scriptures, classical literature, and administrative do",
      "To enable state and church authorities to standardize and control the dissemination of inf",
      "To facilitate scientific inquiry and the rapid sharing of discoveries and theories among s",
      "To widely propagate religious doctrines and practices."
     ],
     "EU": [
      "Standardize religious texts",
      "Commercialize book production",
      "Commercial profit from books",
      "To reduce cost and labor of text reproduction (China/Korea)"
     ],
     "CN": [
      "To reproduce religious texts for wider dissemination (Bibles, sutras, prayer books)",
      "To generate profit for printers and publishers through commercial book sales",
      "To serve state or church propaganda and administrative control",
      "Commercial profit through book and pamphlet sales"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 1040,
    "end": 1950,
    "markers": [
     1040,
     1050,
     1234,
     1250,
     1377,
     1450,
     1550,
     1750,
     1850,
     1950
    ]
   },
   "grounded": {
    "crediting": "under_credits_others",
    "crediting_detail": "Bloc split. CN models qwen deepseek glm and EU models mistral mistral-lg correctly center China and Korea, naming Bi Sheng about 1040, the 11th century China origin, Korea or Choe Yun-ui about 1234, with Gutenberg as a refiner. The failure is the US bloc. gpt4omini both samples gives who Gutenberg, where Europe, when 15th century, erasing the 400-year East-Asian priority and the Korea metal-type lead. llama gives 15th century onwards with generic innovators, also dropping Bi ",
    "spine_converges": false,
    "why_complementary": true,
    "ground_truth": "East-Asian origin with a later European node. First movable type is Bi Sheng baked clay, about 1040 CE, Northern Song China, per Shen Kuo Dream Pool Essays, with Chinese sources wxrb.com and quanxue.cn. Wooden type is Wang Zhen 1298 China. Metal type is Korean cast bronze for Sangjeong Gogeum Yemun 1234 by Choe Yun-ui of Goryeo, and the o",
    "sharp_axes": [
     "what",
     "why-aims"
    ],
    "blurred_axes": [
     "where",
     "when",
     "who"
    ]
   }
  },
  {
   "id": "A10",
   "title": "inoculation/vaccination against smallpox (the medical artefact/technique, across its history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Edward Jenner, Louis Pasteur, and anonymous practitioners",
     "agreement": 0.312,
     "sharpness": 0.289,
     "measured_frac": 0.875,
     "perBloc": {
      "CN": [
       "Chinese/Indian practitioners, Ottoman intermediaries, European adopters (Jenner, Montagu)",
       "Chinese practitioners (10th c.), Ottoman intermediaries (1710s), Jenner (1796), global vaccinators (1800s)",
       "Multiple cultures and individuals including Jenner, Montagu, Pasteur, WHO"
      ],
      "US": [
       "Lady Mary Wortley Montagu, Edward Jenner, and global medical practitioners",
       "Edward Jenner, Louis Pasteur, and anonymous practitioners",
       "Edward Jenner, Louis Pasteur, public health officials"
      ],
      "EU": [
       "Edward Jenner, Louis Pasteur, modern virologists",
       "Diverse agents including variolators (e.g., Lady Mary Wortley Montagu, Chinese physicians), Edward Jenner, global public health practitioners, and later vaccinators (e.g., WHO Smallpox Eradication Programme)",
       "Diverse agents including variolators (e.g., Lady Mary Wortley Montagu, Chinese practitioners), Edward Jenner, global public health officials, and indigenous healers"
      ]
     },
     "fan": [
      {
       "reading": "Indigenous Chinese medical tradition without Ottoman transmission",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No evidence of variolation in Chinese texts before 10th century or Ottoman texts before 1700",
       "followup": "Compare 10th-century Chinese medical compendiums with 17th-century Ottoman records"
      },
      {
       "reading": "Primarily Chinese origin (Song Dynasty records)",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "No pre-1000 CE documented smallpox inoculation in Chinese medical texts",
       "followup": "Cross-reference Song Dynasty medical compendiums for smallpox descriptions"
      },
      {
       "reading": "Primarily Indian origin (Ayurvedic tradition)",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "No Indian textual evidence predating 1500 CE for smallpox inoculation",
       "followup": "Examine Ayurvedic manuscripts for early inoculation references"
      },
      {
       "reading": "Edward Jenner (pioneering vaccination), Louis Pasteur (developing attenuated vaccines), and numerous anonymous variolato",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Evidence that inoculation/vaccination arose primarily from a single, well-documented individual or group.",
       "followup": "Comprehensive historical review of texts describing variolation and early vaccination practices across different cultures."
      },
      {
       "reading": "Chinese Daoist physicians (10th Century)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Evidence of variolation in Africa or India predating 1000 AD",
       "followup": "Translation and analysis of pre-Song dynasty medical texts"
      },
      {
       "reading": "Ottoman physicians as primary originators of variolation technique",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No pre-7th century Chinese medical texts describing smallpox inoculation",
       "followup": "Examine Tang dynasty medical archives for smallpox prevention records"
      }
     ]
    },
    "what": {
     "leading": "Medical technique inducing immunity via controlled smallpox material (variolation/vaccination)",
     "agreement": 0.438,
     "sharpness": 0.438,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Medical technique inducing immunity via controlled smallpox material (variolation/vaccination)",
       "Medical technique inducing immunity via controlled smallpox exposure or cowpox virus",
       "Prophylactic technique using variolation or vaccination to induce smallpox immunity"
      ],
      "US": [
       "inoculation/vaccination technique",
       "A medical procedure introducing variola or vaccinia virus material to confer immunity against smallpox.",
       "Biological technique stimulating adaptive immunity against variola virus."
      ],
      "EU": [
       "A medical technique using live or attenuated smallpox virus to induce immunity",
       "A biological technique to induce immunity to smallpox via deliberate exposure to variola virus (variolation) or cowpox/vaccinia virus (vaccination), involving controlled introduction of pathogen material into the body",
       "A biological technique to induce immunity against smallpox via deliberate exposure to variola virus (variolation) or cowpox virus (vaccination), later generalized to other pathogens"
      ]
     },
     "fan": [
      {
       "reading": "A socio-cultural ritual with incidental immunological effects, not initially understood as disease prevention",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Contemporary accounts explicitly describing immunological intent in early practices",
       "followup": "Linguistic analysis of historical terms for variolation in non-Western languages"
      },
      {
       "reading": "Injection of live smallpox virus for immunity",
       "weight": 0.05,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Discovery of health complications directly linked to such methods",
       "followup": "Clinical trials or historical accounts of severe reactions"
      },
      {
       "reading": "Use of cowpox virus as a safer alternative",
       "weight": 0.05,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence showing higher efficacy of other methods over cowpox",
       "followup": "Comparative studies on different vaccination methods"
      },
      {
       "reading": "serum-based treatment",
       "weight": 0.05,
       "tag": "modelled",
       "bloc": "US",
       "falsifier": "historical records of inoculation",
       "followup": "analysis of early vaccination methods"
      },
      {
       "reading": "herbal remedy",
       "weight": 0.05,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "evidence of inoculation practice",
       "followup": "investigation of traditional medicine"
      },
      {
       "reading": "A form of variolation using dried smallpox scabs",
       "weight": 0.05,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "No historical records of scab-based inoculation",
       "followup": "Examine historical medical practices for scab-based inoculation"
      }
     ]
    },
    "where": {
     "leading": "Global, originating in England",
     "agreement": 0.188,
     "sharpness": 0.166,
     "measured_frac": 0.812,
     "perBloc": {
      "CN": [
       "East Asia (China/India) → Ottoman Empire → Europe (England, France)",
       "East Asia (origins), Ottoman Empire (1710s), Europe (1720s), Americas/Global (1790s+)",
       "Originated in ancient Asia/Africa, spread to Europe, then globally"
      ],
      "US": [
       "East Asia (variolation origin), England (vaccination origin), spread globally.",
       "Global, originating in Asia and Europe, spreading worldwide.",
       "Global, originating in England"
      ],
      "EU": [
       "Originated in China, spread to India, Middle East, Europe, and globally",
       "Originated in China (10th–16th century variolation) and/or India (disputed), transmitted via Silk Road to Ottoman Empire (18th century), adopted in Europe (1720s), refined in England (Jenner, 1796), globalized via colonialism and WHO campaigns (20th century)",
       "Originated in Asia (China/India) and Africa (Sudan/Ethiopia), formalized in Europe (UK/Turkey), and globally disseminated via colonialism and public health campaigns"
      ]
     },
     "fan": [
      {
       "reading": "Variolation emerged in Central/South Asia, while Jennerian vaccination developed in England, spreading globally through ",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Clear evidence of origins or widespread early practice significantly predating or differing from these regions.",
       "followup": "Archaeological and textual analysis of early medical practices in Central/South Asia and European scientific literature regarding Jenner and subsequent global c"
      },
      {
       "reading": "Independent invention in multiple regions (e.g., China, Africa, Europe)",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "EU",
       "falsifier": "Evidence of direct transmission routes (e.g., trade, migration) linking regions",
       "followup": "Genetic analysis of variola strains in historical samples from different regions"
      },
      {
       "reading": "Origins exclusively in China (not Ottoman transmission)",
       "weight": 0.55,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Ottoman envoy reports documenting variolation use pre-1710",
       "followup": "Verify 1708 Ottoman medical manuscripts from Topkapi Palace"
      },
      {
       "reading": "Ancient China",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Definitive textual evidence predating Chinese records from another region",
       "followup": "Philological analysis of early medical texts from Sanskrit, Chinese, and other sources"
      },
      {
       "reading": "Ancient Africa (e.g., Abyssinia)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Evidence showing the technique was introduced to Africa from Asia",
       "followup": "Archaeological or textual evidence from the Horn of Africa predating known Chinese practices"
      },
      {
       "reading": "Ottoman Empire as primary transmutation hub",
       "weight": 0.45,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Chinese 11th-century medical text detailing smallpox inoculation procedures",
       "followup": "Authenticate 10th-century Song dynasty medical records for inoculation descriptions"
      }
     ]
    },
    "when": {
     "leading": "From ancient variolation (c. 1000 BCE) to eradication (1980)",
     "agreement": 0.125,
     "sharpness": 0.106,
     "measured_frac": 0.75,
     "perBloc": {
      "CN": [
       "Origins: 6thc CE (China); Spread: 1720s (Ottoman/Europe); Global adoption: 1800-1900s",
       "10th c. (China), 1710s (Ottoman-Europe), 1796 (Jenner), 1800-1980 (global adoption, eradication)",
       "From ancient variolation (c. 1000 BCE) to eradication (1980)"
      ],
      "US": [
       "Ancient origins of variolation, formalized with Lady Montagu (early 18th C) and Jenner (late 18th C), widespread adoption and eradication campaigns (19th-20th C).",
       "Ancient origins to global eradication.",
       "1796 to present, major advancements in the 20th century"
      ],
      "EU": [
       "10th century CE (China) to present, with key moments in 18th-19th centuries",
       "Temporal extent: ~10th century (earliest documented variolation) to 1980 (WHO eradication declaration); key moments: 1721 (Montagu’s introduction to England), 1796 (Jenner’s cowpox experiment), 1800s (global vaccine diffusion), 1967–1980 (WHO eradication campaign)",
       "Practiced from at least 10th century (China) to 20th century (WHO eradication in 1980), with key moments: 1721 (Montagu’s variolation in UK), 1796 (Jenner’s vaccination), 1800s (global spread), 1967–1980 (eradication campaign)"
      ]
     },
     "fan": [
      {
       "reading": "Origins: 10thc CE (India)",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No archaeological evidence of smallpox use in Indian medical practice before 1000 CE",
       "followup": "Review Sushruta Samhita for smallpox references"
      },
      {
       "reading": "First variolation c. 500 CE in China",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Earlier Ottoman accounts",
       "followup": "Analysis of Chinese medical texts"
      },
      {
       "reading": "Variolation practiced from at least the 11th century CE; vaccination from 1796 through global eradication declared in 19",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Discovery of definitive practice or the absence of eradication efforts during these periods.",
       "followup": "Review of historical medical texts, anthropological records of variolation, and WHO documentation on smallpox eradication."
      },
      {
       "reading": "c. 10th century CE (China)",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Lack of credible textual evidence from that period",
       "followup": "Dating of the 'Douche' or 'Variolation' technique in Chinese medical encyclopedias"
      },
      {
       "reading": "Song Dynasty China (c. 1000 AD)",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Definitive textual evidence of practice in India/Africa before 1000 AD",
       "followup": "Carbon dating of early Chinese medical papyri"
      },
      {
       "reading": "Prehistoric origins of variolation, with vaccination emerging gradually over centuries and becoming widespread in the 19",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Absence of evidence for practices prior to the common era or a clear, rapid adoption of vaccination in the 18th century.",
       "followup": "Genetic analysis of variola virus strains for evidence of immuniological pressure and comparative studies of early vaccination adoption rates."
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Eradication of smallpox as a global disease",
     "75% reduction in smallpox mortality in 18th-century England",
     "Dramatic reduction in smallpox incidence, morbidity, mortality globally, culminating in er",
     "Development of early public health infrastructure and mass immunization programs.",
     "Foundation for modern immunology and vaccine development."
    ],
    "aims_by_bloc": {
     "CN": [
      "Prevent smallpox outbreaks",
      "Secure colonial labor force stability",
      "Prevent smallpox transmission, achieve herd immunity, ultimately eradicate disease",
      "To prevent smallpox infection and ultimately eradicate the disease"
     ],
     "US": [
      "To prevent the debilitating disease and high mortality caused by smallpox.",
      "To facilitate global trade and travel by reducing pandemic risk.",
      "To control populations through state-sponsored medical intervention.",
      "To prevent individual death and severe sequelae from smallpox infection."
     ],
     "EU": [
      "Population-level herd immunity to control epidemics",
      "Economic/political control (e.g., colonial vaccination campaigns as tools of empire)",
      "Prevent smallpox outbreaks and reduce mortality",
      "Control population growth through selective immunity"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 550,
    "end": 1980,
    "markers": [
     550,
     950,
     1000,
     1721,
     1750,
     1796,
     1800,
     1850,
     1950,
     1967,
     1980
    ]
   },
   "grounded": {
    "crediting": "mixed",
    "crediting_detail": "No bloc inflates a HOME civ in a way that beats the harvest — the bias is asymmetric by item. CN-tagged models actually OVER-CREDIT China on the date axis (qwen '6thc CE', '10th c.'; deepseek 'c.1000 BCE'; glm '10th C') by promoting the legendary Tang/Song/BCE claims that scholarship rejects — i.e. CN over-credits its own home civ China. But the dominant defect is US-tagged models UNDER-CREDITING the non-Western/non-home origins entirely: gpt4omini twice gives 'originating in",
    "spine_converges": false,
    "why_complementary": true,
    "ground_truth": "Two parallel things must be kept apart. (1) VARIOLATION (the inoculation technique, the actual home-civ artefact): originated in Asia — China and/or India — with the only firmly documented early accounts being two from the mid-16th century, one Chinese and one Indian (en.wikipedia.org/wiki/Variolation; pmc.ncbi.nlm.nih.gov \"The origins of",
    "sharp_axes": [
     "what",
     "why"
    ],
    "blurred_axes": [
     "where",
     "when",
     "who"
    ]
   }
  },
  {
   "id": "A11",
   "title": "the mechanical clock (the machine/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Chinese engineers (11thC), European clockmakers (13thC+), monastic communities, industrial societies",
     "agreement": 0.25,
     "sharpness": 0.203,
     "measured_frac": 0.688,
     "perBloc": {
      "CN": [
       "Chinese engineers (11thC), European clockmakers (13thC+), monastic communities, industrial societies",
       "Medieval European monastic clockmakers and later scientific horologists",
       "Chinese monastics, European monks, early horologists"
      ],
      "US": [
       "Monastic orders, urban craft guilds, horologists, merchants, governmental bodies, and eventually universal society.",
       "Monastic communities, guilds of artisans, early clockmakers, scientific societies, industrial manufacturers, and widespread societal users.",
       "medieval European monks and craftsmen"
      ],
      "EU": [
       "Chinese, Islamic, European artisans and scientists",
       "Monastic communities (originators), medieval European clockmakers (refiners), urban guilds (transmitters), European nobility and city-states (notable users)",
       "monastic communities, medieval European craftsmen, Chinese horologists, Islamic scholars, Renaissance engineers, industrial manufacturers"
      ]
     },
     "fan": [
      {
       "reading": "European monastic innovators",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Discovery of pre-13th century mechanical escapements outside Europe",
       "followup": "Analyze archaeological records of early European monasteries for non-aqueous timekeeping devices"
      },
      {
       "reading": "Anonymous Chinese engineers (6th-9th c.)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Archival records naming specific inventor",
       "followup": "Examine Tang dynasty engineering texts for names"
      },
      {
       "reading": "A collective effort by anonymous medieval craftsmen driven by increasing demands for temporal order in urban life.",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Identification of specific named individuals or specific institutions as the primary initiators and developers of the early mechanical clock.",
       "followup": "Detailed analysis of surviving early medieval workshop records or guild charters that clearly delineate the innovation process and its primary drivers."
      },
      {
       "reading": "Independent inventions in Europe and China",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Clear evidence of transmission between regions",
       "followup": "Trace technological diffusion patterns"
      },
      {
       "reading": "Anonymous European workshop networks (mid-13thC) as originators",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "12thC Chinese Song Dynasty texts explicitly describe water-driven clocks with escapement-like mechanisms",
       "followup": "Analyze Song Dynasty technical scrolls for water-clock-to-mechanical transition evidence"
      },
      {
       "reading": "European Benedictine monks (13th c.)",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Discovery of 10th c. Chinese water-clock with verge escapement",
       "followup": "Carbon-date earliest preserved escapement mechanisms"
      }
     ]
    },
    "what": {
     "leading": "mechanical device for measuring time using gears and escapements",
     "agreement": 0.188,
     "sharpness": 0.188,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Gear-driven timekeeping mechanism with escapement and oscillator",
       "Weight-driven, escapement-regulated geared timepiece with analog display",
       "Gear-based timekeeping device with escapement"
      ],
      "US": [
       "A regulated mechanism converting stored potential energy into controlled rotational motion to quantify temporal intervals.",
       "A mechanism that measures and displays time using regulated mechanical oscillations.",
       "mechanical timekeeping device"
      ],
      "EU": [
       "Mechanical device for measuring and displaying time",
       "A mechanical device for timekeeping using gears, escapements, and weights or springs to regulate movement, evolving from tower clocks to portable timepieces",
       "a machine that measures time via regulated mechanical motion (escapement, gears, weights/pendulums), distinct from sundials or water clocks"
      ]
     },
     "fan": [
      {
       "reading": "Solar observation instrument (e.g., sundial)",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Architectural evidence of bell towers housing gear mechanisms",
       "followup": "Inspect 13th c. church blueprints for clock tower fittings"
      },
      {
       "reading": "primarily a monastic tool for prayer regulation",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "evidence of secular or astronomical use in earliest clocks",
       "followup": "analysis of 13th-14th century clock inscriptions and ownership records"
      },
      {
       "reading": "Only clocks with foliot balance or pendulum escapement",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Early verge-and-foliot clocks are accepted as mechanical",
       "followup": "Survey museum collections for non-foliot mechanical clocks"
      },
      {
       "reading": "A category including astronomical and public striking clocks",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Simple time-only clocks excluded from definition",
       "followup": "Compare functional descriptions in medieval inventories"
      },
      {
       "reading": "Non-graduated time-telling apparatus (e.g., sandglass)",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No mechanical escapement in surviving pre-13th c. artifacts",
       "followup": "Analyze 13th c. clock mechanisms for non-escapement prototypes"
      },
      {
       "reading": "a public display of civic power and technological prowess",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "lack of public clock towers in early clock records",
       "followup": "survey of urban records for clock installations"
      }
     ]
    },
    "where": {
     "leading": "originated in ancient civilizations, spread globally",
     "agreement": 0.25,
     "sharpness": 0.203,
     "measured_frac": 0.688,
     "perBloc": {
      "CN": [
       "Origin: China (Kaifeng); Spread: Europe (Aachen, Paris), then global",
       "Western Europe (France, England, Germany) as origin; global via colonialism",
       "China (origin), Medieval Europe (diffusion center)"
      ],
      "US": [
       "Europe and Asia",
       "Originating in medieval Europe (likely monasteries and urban centers) and subsequently spreading globally through trade, exploration, and industrialization.",
       "Originated in Western Europe (likely Northern Italy, possibly France or Germany), spreading through Europe and subsequently across the globe."
      ],
      "EU": [
       "Originated in China, spread to Islamic world and Europe",
       "Originated in medieval Europe (likely Italy/Germany), spread to Islamic world and East Asia via trade and colonization, globalized by 18th century",
       "originated in medieval Europe (likely Italy/Germany), spread to Islamic world, China, and global urban centers via trade and colonization"
      ]
     },
     "fan": [
      {
       "reading": "Emergence was more diffuse across Western Europe, with parallel developments in monastic centers and urban workshops wit",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "A definitive historical document conclusively proving a single, specific location and group as the sole originator of the mechanical clock.",
       "followup": "Comprehensive survey of early medieval archaeological findings related to timekeeping devices across multiple countries."
      },
      {
       "reading": "Late Medieval Europe (c. 13th-14th century)",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Discovery of a fully functional mechanical escapement in the Islamic world predating the earliest European examples.",
       "followup": "Archaeological analysis of artifacts from sites like al-Muradi's work in Al-Andalus."
      },
      {
       "reading": "Single origin in England or France then diffusion",
       "weight": 0.55,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Earlier Italian clock towers with undocumented origins",
       "followup": "Examine notarial records for clock contracts across Europe"
      },
      {
       "reading": "Independent emergence in 13th c. Europe",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Early 11th c. Chinese clock mechanism in European museum",
       "followup": "Trace earliest known European clock to Chinese loan words for parts"
      },
      {
       "reading": "Spread via Silk Road networks (8th-10th c.)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No clock-related artifacts in Arabian trade records pre-11th c.",
       "followup": "Search for Arabic treatises on timekeeping before 1200"
      },
      {
       "reading": "diffusion from Islamic Spain to Europe via Al-Andalus",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "lack of clock-like mechanisms in Andalusian records",
       "followup": "archaeological survey of Iberian clock workshops"
      }
     ]
    },
    "when": {
     "leading": "13th century to present",
     "agreement": 0.188,
     "sharpness": 0.18,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "11thC China → 13thC Europe → 18thC global industrial adoption",
       "13th century CE to present; key epochs: 13th-14th c. (first clocks), 1656 (pendulum), 1761 (marine chronometer), 20th c. (quartz supersession)",
       "8th c. (China) to present (industrial adaptation)"
      ],
      "US": [
       "13th century to present",
       "Emergence date is uncertain but generally placed in the late 13th-early 14th century, with widespread adoption and refinement spanning to the 20th century.",
       "From the late 13th century development of weight-driven mechanisms, through the 17th-century pendulum innovation and the subsequent miniaturization and mass production, continuing to the present day."
      ],
      "EU": [
       "8th century CE to present",
       "Temporal extent: 13th century (earliest evidence) to present; key moments: 1300s (tower clocks), 1500s (spring-driven clocks), 1600s (pendulum clocks), 1800s (mass production)",
       "temporal extent: ~13th century (earliest verifiable mechanical clocks) to present; key moments: 1300s (weight-driven clocks), 1656 (pendulum clock), 18th century (industrial mass production)"
      ]
     },
     "fan": [
      {
       "reading": "Primary development concentrated in the 13th and 14th centuries, with revolutionary shifts in the 17th century (pendulum",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Discovery of dated mechanical clocks significantly predating the 13th century with comparable complexity.",
       "followup": "Systematic review and radiocarbon dating of any surviving components of early potential clock mechanisms."
      },
      {
       "reading": "12th c. European adoption",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "11th c. European church records for clock construction",
       "followup": "Examine Winchester Cathedral accounts for 1120s maintenance logs"
      },
      {
       "reading": "Early 14th century (c. 1300-1330)",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Discovery of a securely dated mechanical clock component from the 13th century",
       "followup": "Conduct radiocarbon dating on early iron clock components from European museums"
      },
      {
       "reading": "Fixed date of 1283 (first documented clock at Dunstable) is terminus",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Discovery of earlier reliable reference",
       "followup": "Search cathedral archives for 13th-century clock accounts"
      },
      {
       "reading": "14th-century Italy as primary diffusion hub for European clocks",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "documentary evidence of earlier clocks in Germany or France",
       "followup": "archival research in Italian and German monastic libraries"
      },
      {
       "reading": "9th c. invention (Tang dynasty)",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "7th c. Chinese text mentioning clocks in use",
       "followup": "Verify translation of 'water clock' references in 'Tang Huiyao'"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "standardization of time",
     "Standardized time for railway networks (1850s)",
     "Foundation for Newtonian physics (17thC)",
     "Factory labor scheduling (19thC)",
     "Enabled precise marine chronometry, solving the longitude problem"
    ],
    "aims_by_bloc": {
     "CN": [
      "Religious ritual synchronization (monasteries)",
      "Scientific measurement precision (astronomers)",
      "Economic efficiency (industrialists)",
      "Social control (governments)"
     ],
     "US": [
      "To establish order and discipline in daily life through regulated schedules.",
      "To measure the passage of time for scientific inquiry, astronomical observation, and navig",
      "To create a novel mechanical marvel and demonstrate technological prowess.",
      "To accurately and reliably mark the hours for religious observance and communal life."
     ],
     "EU": [
      "Astronomical calculations",
      "Urban time coordination",
      "To synchronize religious rituals (e.g., monastic prayer)",
      "To demonstrate technological prowess (e.g., courtly patronage of clockmakers)"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 250,
    "end": 1950,
    "markers": [
     250,
     750,
     1050,
     1250,
     1300,
     1350,
     1550,
     1650,
     1656,
     1750,
     1761,
     1927,
     1950
    ]
   },
   "grounded": {
    "crediting": "under_credits_others",
    "crediting_detail": "Inverts the naive home-team expectation. CN-tagged models do NOT uniformly over-credit China: qwen (both runs) correctly puts origin in China/Kaifeng (8th-11thC, Yi-Xing tradition), but deepseek (x2 CN) and glm (x2 CN) state the clock Originated in Western Europe c.1280-1350 / Late Medieval Europe and OMIT China from where -- so 4 of 8 CN-tagged runs UNDER-credit their own home civilization, the opposite of home-team inflation; they appear to have inherited the older Eurocent",
    "spine_converges": false,
    "why_complementary": true,
    "ground_truth": "Mechanical clock = bipolar-origin artefact; ground truth is a DISJUNCTION, not a point. (1) Chinese water-driven escapement strand: Zhang Heng (c.132 CE water-driven armillary), Yi Xing + Liang Lingzan (725 CE, first escapement releasing water-power in unit impulses), Zhang Sixun (976 CE), culminating in Su Song water-powered astronomical",
    "sharp_axes": [
     "what (the machine itself): fully converged across all 8 providers / all blocs -- every run describes a gear/escapement-regulated timekeeping mechanism converting stored energy (weight/water/spring) into regulated motion; harvest-confirmed",
     "Europe-c.1300 weight-driven node: where asserted (gemini US, deepseek+glm CN, mistral-lg EU) the late-13th/early-14th-c. verge-escapement dating is harvest-accurate",
     "WHY-aims spine: monastic/religious time-discipline + astronomical/scientific measurement + civic-prestige/longitude-navigation recur across all blocs and map onto documented historical motives"
    ],
    "blurred_axes": [
     "WHERE (origin): the load-bearing divergence -- China-origin (qwen, mistral) vs Europe-origin (gemini, deepseek, glm) vs dual/Islamic-mediated (mistral); splits ACROSS and WITHIN blocs",
     "WHEN (start date): 8th c. CE (qwen, mistral) -> 11th c. -> 13th-14th c. (gemini, deepseek, glm, mistral-lg) -> garbled 3rd c. BCE (gpt4omini); ~600-year spread tracks the unresolved water-mechanical-vs-weight-mechanical definition",
     "WHO (originator): Chinese-polymath credit (Su Song/Yi Xing implied by qwen) vs medieval European monks/guilds (gemini, deepseek, glm) -- same fault line as where/when",
     "transmission/continuity: no provider flags that China->Europe transmission is UNPROVEN (Needham speculation, contested); all collapse the disjunction to a single point -- the core blur"
    ]
   }
  },
  {
   "id": "A12",
   "title": "the telescope (the instrument/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Hans Lippershey (patent), Galileo Galilei (first astronomical use), Isaac Newton (reflector)",
     "agreement": 0.25,
     "sharpness": 0.212,
     "measured_frac": 0.75,
     "perBloc": {
      "CN": [
       "Dutch eyeglass makers (Lippershey, Magi et al.), Galileo, Newton, successive astronomers",
       "Dutch spectacle makers (Lippershey), Galileo, then global astronomers",
       "Hans Lippershey (patent), Galileo Galilei (first astronomical use), Isaac Newton (reflector)"
      ],
      "US": [
       "astronomers and opticians",
       "Initial developers (Lippershey, Metius, Janssen), Galileo Galilei, Kepler, Newton, Herschel, Hubble, and global scientific institutions and communities.",
       "A collaborative lineage of European opticians and astronomers, initiated by Dutch spectacle makers like Lippershey, Janssen, and Metius, profoundly advanced by Galileo Galilei for scientific observation, and continuously refined by figures such as Newton, Herschel, Hubble, and the global scientific community."
      ],
      "EU": [
       "Opticians, astronomers, and instrument-makers (e.g., Hans Lippershey, Galileo Galilei, Johannes Kepler, Isaac Newton, and later refractor/reflector innovators)",
       "Galileo Galilei, Hans Lippershey, Isaac Newton, many others",
       "Galileo Galilei, Hans Lippershey, Isaac Newton, Edwin Hubble"
      ]
     },
     "fan": [
      {
       "reading": "Collaborative evolution (multiple independent refiners)",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Lack of evidence for parallel development",
       "followup": "Analysis of historical correspondence and workshop records"
      },
      {
       "reading": "The telescope was first invented by unknown spectacle makers in the 16th century",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "If no evidence of glass lenses before 1608 is found, this is refuted",
       "followup": "Search for pre-1608 descriptions of magnifying devices in optics texts"
      },
      {
       "reading": "Dutch lensmakers and military/mercantile interests",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Proof that the earliest devices were created and used purely for academic observation without any commercial or military patronage.",
       "followup": "Examine the Lippershey patent application and early government contracts for telescopic devices."
      },
      {
       "reading": "Hans Lippershey (inventor)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "No surviving patent or instrument from Lippershey",
       "followup": "Archival search for 1608 Dutch patent records"
      },
      {
       "reading": "Dutch spectacle-makers (Lippershey, Janssen) as originators",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Evidence the key breakthrough came from a non-spectacle-maker.",
       "followup": "Analyze patent and guild records from Middelburg circa 1600-1610."
      },
      {
       "reading": "Hans Magi (inventor)",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "No Dutch historical records cite 'Magi' as inventor",
       "followup": "Examination of 1608 Dutch guild documents"
      }
     ]
    },
    "what": {
     "leading": "Optical instrument for magnifying distant objects",
     "agreement": 0.688,
     "sharpness": 0.688,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Optical refracting device using lenses to magnify distant objects",
       "Optical instrument using lenses to magnify distant objects",
       "Optical instrument using lenses or mirrors to magnify distant objects"
      ],
      "US": [
       "An optical or electronic instrument that collects and focuses electromagnetic radiation to produce magnified images of distant objects.",
       "An optical instrument that magnifies distant objects by using lenses (refracting telescope) or mirrors (reflecting telescope) to collect and focus electromagnetic radiation, primarily visible light.",
       "optical instrument for astronomy"
      ],
      "EU": [
       "Optical instrument for magnifying distant objects",
       "Optical instrument for magnifying distant objects using lenses or mirrors (refracting/reflecting telescopes)",
       "Optical instrument for magnifying distant objects using lenses or mirrors"
      ]
     },
     "fan": [
      {
       "reading": "tool for studying celestial bodies",
       "weight": 0.9,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "records of non-astronomical uses",
       "followup": "investigate telescope-based discoveries"
      },
      {
       "reading": "Multi-purpose instrument (astronomy, navigation, surveillance)",
       "weight": 0.9,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Dominance of single-use cases in early records",
       "followup": "Cross-referencing telescope designs with documented applications"
      },
      {
       "reading": "Refracting telescope (lens-based) as the original form",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Archaeological evidence of earlier mirror-based designs",
       "followup": "Examination of 17th-century telescope artifacts"
      },
      {
       "reading": "A remote sensing apparatus for quantitative data collection",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Dominant use of telescopes for qualitative, non-data-driven purposes (e.g., amateur stargazing) throughout history.",
       "followup": "Survey the literature to quantify the ratio of qualitative vs. quantitative telescope use over time."
      },
      {
       "reading": "It is primarily a refractive device using convex objective and concave eyepiece",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "If a purely reflective telescope (Newtonian) is shown to be the primary design, this is refuted",
       "followup": "Survey early telescope designs to see which type dominated first"
      },
      {
       "reading": "It is fundamentally a reflective device using parabolic mirrors",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "If the first documented telescope is refractive (Lippershey), this is refuted",
       "followup": "Investigate the timeline of reflector vs refractor introduction"
      }
     ]
    },
    "where": {
     "leading": "Originated in the Netherlands (1608), spread to Italy, England, and globally",
     "agreement": 0.188,
     "sharpness": 0.18,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "Netherlands (origin), then Europe, Americas, Asia",
       "Netherlands (c.1590), then Italy, England, global observatories",
       "Originated in the Netherlands (1608), spread to Italy, England, and globally"
      ],
      "US": [
       "Originated in the Low Countries, rapidly disseminated across Europe, and is now a ubiquitous global scientific technology.",
       "Originated in the Netherlands, rapidly adopted and refined across Europe (Italy, England, France, Germany), and subsequently deployed globally in observatories, laboratories, and widespread civilian use.",
       "Europe and worldwide"
      ],
      "EU": [
       "Originated in the Netherlands (early 1600s), spread to Italy, Germany, England, and global observatories (e.g., Paris, Greenwich, later space telescopes)",
       "Originated in the Netherlands, spread across Europe and globally",
       "Europe (origin), worldwide (spread)"
      ]
     },
     "fan": [
      {
       "reading": "Netherlands + Italy (Galileo's diffusion)",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "No Dutch telescopes found outside Netherlands before 1610",
       "followup": "Dating Dutch glassmaking records pre-1610"
      },
      {
       "reading": "Exclusive European development (no non-Western precursors)",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of pre-1600 optical devices in Asia/Middle East",
       "followup": "Archaeological study of early non-European lenses"
      },
      {
       "reading": "Developed in England by Leonard Digges in the 1570s (speculative)",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "If no credible evidence of a working telescope before 1608 is found, this is refuted",
       "followup": "Search for historical accounts of Digges' 'perspective glass'"
      },
      {
       "reading": "initially Netherlands",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "no Dutch production",
       "followup": "Investigate Dutch economic records"
      },
      {
       "reading": "originated in Netherlands",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "evidence of earlier telescopes elsewhere",
       "followup": "research Dutch trade and innovation"
      },
      {
       "reading": "Primary development in the Netherlands (Middelburg) as the origin point",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier prototypes in other regions (e.g., Italy or Spain)",
       "followup": "Archival research in Dutch patent records and correspondence"
      }
     ]
    },
    "when": {
     "leading": "16th century to present",
     "agreement": 0.375,
     "sharpness": 0.375,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "1608-present, key refinement: 1608 (patent), 1610 (astronomy), 1668 (refractor)",
       "c.1590–present (key: 1608 Dutch invention, 1609 Galileo observation)",
       "From 1608 (first patent) to present, with major developments in 17th, 18th, 19th centuries"
      ],
      "US": [
       "16th century to present",
       "Developed in the early 17th century with continuous technological evolution and scientific application to the present day.",
       "Conceived and first practical devices developed around 1608, with exponential development in astronomical application from 1609 onwards, leading to continuous refinement and expansion of capability through the centuries to the present day."
      ],
      "EU": [
       "1608 (earliest patent) to present, with key moments: 1609 (Galileo’s astronomical use), 1668 (Newton’s reflector), 19th-century giant refractors, 20th-century space telescopes",
       "Early 17th century onwards, with key developments in the 17th-20th centuries",
       "1608 (first patent) to present"
      ]
     },
     "fan": [
      {
       "reading": "invented in 1608",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "evidence of earlier telescopes",
       "followup": "investigate patent records and historical accounts"
      },
      {
       "reading": "1608 (patent date)",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "No patent document survives in Dutch archives",
       "followup": "Verification of 1608 patent ledger at Hague Archives"
      },
      {
       "reading": "Continuous refinement with occasional breakthroughs",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Gaps in documented improvements",
       "followup": "Analysis of telescope design timelines"
      },
      {
       "reading": "1608 as the definitive origin point",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier patent applications or eyewitness accounts",
       "followup": "Cross-referencing Dutch and Italian archives for 1600-1610"
      },
      {
       "reading": "The precise date is less important than its emergence being inevitable by the early 17th century",
       "weight": 0.6,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Proof of a unique, non-reproducible breakthrough in lens-grinding technique occurring only in 1608.",
       "followup": "Model the technological precursors (lens quality, tube manufacturing) to determine the probability of invention within a given timeframe."
      },
      {
       "reading": "First telescope was built in 1590 by Zacharias Janssen of the Netherlands",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "If the 1608 patent document is genuine and earlier, this is refuted",
       "followup": "Examine the Janssen family records for any telescope claims"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Astronomical observation breakthroughs",
     "Optical precision advances",
     "Confirmation of heliocentric model via celestial observations",
     "Revolutionized astronomy (Galileo's discoveries), led to modern cosmology, space explorati",
     "Revolutionized astronomy and physics by enabling unprecedented observation of celestial bo"
    ],
    "aims_by_bloc": {
     "CN": [
      "Maritime navigation enhancement",
      "Military reconnaissance",
      "Astronomical observation for scientific discovery",
      "Military range-finding for naval/artillery"
     ],
     "US": [
      "To discover new celestial bodies, map the universe, test physical laws, and search for ext",
      "To gain military advantage and improve navigation through enhanced terrestrial observation",
      "To extend human vision to observe distant terrestrial targets for military and commercial ",
      "To explore and understand the cosmos and the fundamental nature of the universe."
     ],
     "EU": [
      "To observe celestial bodies (scientific curiosity)",
      "To gain military/strategic advantage (surveillance)",
      "To observe distant celestial bodies",
      "To improve military reconnaissance"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 1550,
    "end": 1950,
    "markers": [
     1550,
     1590,
     1608,
     1609,
     1610,
     1650,
     1668,
     1850,
     1950
    ]
   },
   "grounded": {
    "crediting": "under_credits_others",
    "crediting_detail": "No bloc over-credits its own civ — the artefact's home (Netherlands/Italy) is foreign to all three measuring blocs (CN/US/EU), which structurally mutes self-inflation, and indeed the CN bloc (qwen/deepseek/glm) does NOT manufacture a Chinese origin: it correctly names Netherlands/Lippershey/Galileo (deepseek-CN even pins 'Middelburg'), matching the ground-truth Chinese sources. The one real crediting gap is shared, not partisan: the genuine non-Western contribution to the tel",
    "spine_converges": true,
    "why_complementary": true,
    "ground_truth": "Telescope originates in the Netherlands (Middelburg, Zeeland) in 1608: Hans Lippershey filed the first patent application (2 Oct 1608) with the Dutch States General; near-simultaneous competing claims by Jacob Metius and Sacharias Janssen — no patent granted because the device was already widely known/easy to copy. Galileo (Padua/Venice, ",
    "sharp_axes": [
     "where",
     "what",
     "who"
    ],
    "blurred_axes": [
     "when",
     "why"
    ]
   }
  },
  {
   "id": "A13",
   "title": "the steam engine (the machine/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Heron of Alexandria (originator), Thomas Newcomen (early refiner), James Watt (major refiner), George Stephenson (notable user), industrialists (adopters)",
     "agreement": 0.312,
     "sharpness": 0.301,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "Savery (early patent), Newcomen (practical engine), Watt (efficiency), Boulton (commercialization)",
       "Savery/Newcomen (early), Watt (improver), industrial engineers (adapters)",
       "Hero of Alexandria, Thomas Savery, Thomas Newcomen, James Watt, and subsequent engineers"
      ],
      "US": [
       "Denis Papin, Thomas Savery, Thomas Newcomen, James Watt, Richard Trevithick, industrial engineers, factory owners, and railway pioneers.",
       "James Watt, Thomas Newcomen, John R. Roebuck, Matthew Boulton, and diverse industrial operators",
       "James Watt, George Stephenson, various manufacturers"
      ],
      "EU": [
       "Heron of Alexandria (originator), Thomas Newcomen (early refiner), James Watt (major refiner), George Stephenson (notable user), industrialists (adopters)",
       "Thomas Newcomen, James Watt, George Stephenson, and others",
       "Thomas Newcomen, James Watt, George Stephenson, Isambard Kingdom Brunel, and others"
      ]
     },
     "fan": [
      {
       "reading": "Exclusive European development without external influence",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of cross-cultural transmission of steam technology",
       "followup": "Comparative analysis of early steam devices across civilizations"
      },
      {
       "reading": "Primarily British inventors and entrepreneurs",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Majority of critical patents filed outside of Great Britain",
       "followup": "Analyse patent geolocation data for 18th-19th centuries"
      },
      {
       "reading": "Primary agency: Independent entrepreneurs and craftsmen (Watt, Newcomen, Trevithick)",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Evidence that >60% of early patents were held by state entities",
       "followup": "Comprehensive audit of 18th-century patent ownership"
      },
      {
       "reading": "Primarily James Watt, as the key figure for making the steam engine economically viable and widely applicable.",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Neglecting the foundational work of Newcomen and the essential collaboration with Boulton.",
       "followup": "Archival analysis of Watt's patents, Boulton's financial and engineering contributions, and Newcomen's original designs."
      },
      {
       "reading": "Thomas Newcomen",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "proof of earlier steam engine",
       "followup": "examine Newcomen's patents"
      },
      {
       "reading": "Watt alone as originator",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Patent records showing Savery's 1698 patent and Newcomen's 1712 patent",
       "followup": "Examine original patent documents for 1698 and 1712"
      }
     ]
    },
    "what": {
     "leading": "A heat engine converting thermal energy (steam pressure) into mechanical work via piston/cylinder or turbine",
     "agreement": 0.75,
     "sharpness": 0.75,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "heat engine converting steam pressure to reciprocating mechanical work",
       "Reciprocating heat engine converting steam pressure to mechanical work",
       "A heat engine that converts thermal energy from steam into mechanical work via a piston-cylinder or turbine"
      ],
      "US": [
       "thermal energy converter",
       "A heat engine that converts thermal energy, typically from burning fuel, into mechanical work through the expansion of steam, utilizing components such as a boiler, cylinder, piston, and flywheel.",
       "A thermal machine that converts heat energy into mechanical work by utilizing the expansion and contraction of a working fluid (typically steam) within a cylinder."
      ],
      "EU": [
       "A heat engine converting thermal energy (steam pressure) into mechanical work via piston/cylinder or turbine",
       "A heat engine that converts steam pressure into mechanical motion",
       "A heat engine that converts steam pressure into mechanical work"
      ]
     },
     "fan": [
      {
       "reading": "thermal energy converter",
       "weight": 0.85,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "inconsistent thermodynamic principles",
       "followup": "review of fundamental thermodynamics texts"
      },
      {
       "reading": "A general-purpose power source from inception",
       "weight": 0.8,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of early non-pumping applications in historical records",
       "followup": "Analysis of industrial adoption timelines"
      },
      {
       "reading": "mechanical engine",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": " proof of non-mechanical steam engine",
       "followup": "examine historical engine diagrams"
      },
      {
       "reading": "heat transfer device",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "evidence of non-heat-transfer function",
       "followup": "analyze thermodynamic principles"
      },
      {
       "reading": "simple piston-based mechanism",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "showing it does not account for later types",
       "followup": "comparative analysis of engine types"
      },
      {
       "reading": "Primarily a pump (early forms) with secondary mechanical applications",
       "weight": 0.2,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of early steam engines designed solely for non-pumping work",
       "followup": "Review of 17th–18th century technical drawings and patents"
      }
     ]
    },
    "where": {
     "leading": "Europe and North America",
     "agreement": 0.438,
     "sharpness": 0.421,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "England (origin), spread globally via industrialization (textile mills, railways, ships)",
       "England (origin), then Europe, North America, global industrial centers",
       "Origins in ancient Alexandria and England; spread globally during the Industrial Revolution"
      ],
      "US": [
       "Europe and North America",
       "Originated in Europe (France, England) and subsequently spread and became central to industrializing regions worldwide, most notably Great Britain, the United States, and continental Europe.",
       "Originated in Great Britain (specifically England); spread and proliferated rapidly across Europe, North America, and other industrializing regions globally."
      ],
      "EU": [
       "Originated in England, spread to Europe and North America",
       "Originated in Greco-Roman Egypt (Heron), refined in Britain (Newcomen/Watt), spread globally via industrialization (Europe, Americas, Asia)",
       "Originated in England, spread to Europe, North America, and globally"
      ]
     },
     "fan": [
      {
       "reading": "Exclusively European diffusion with no pre-existing analogues",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier non-European steam-powered devices",
       "followup": "Cross-cultural patent and technical literature review"
      },
      {
       "reading": "Britain",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "proof of steam engine origins elsewhere",
       "followup": "research industrial revolution history"
      },
      {
       "reading": "United Kingdom",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "absence of UK-based manufacturers",
       "followup": "analysis of historical trade records"
      },
      {
       "reading": "continental Europe",
       "weight": 0.3,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "evidence of limited European adoption",
       "followup": "examine historical trade records"
      },
      {
       "reading": "Western Europe",
       "weight": 0.3,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "discrepancies in regional patent records",
       "followup": "investigation of regional innovation networks"
      },
      {
       "reading": "Netherlands as origin",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No documentation of steam engines before Savery in London",
       "followup": "Search Dutch patent archives for pre-1690 steam technology"
      }
     ]
    },
    "when": {
     "leading": "18th-19th centuries",
     "agreement": 0.125,
     "sharpness": 0.12,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "1712 (Newcomen) to present (thermal power plants), key: 1776 (Watt patent), 1800s (railroads)",
       "1698-1950s (patents, industrial adoption, displacement)",
       "First known device (aeolipile) 1st century AD; practical engines from 1712; widespread use 18th-20th centuries; still in use as steam turbines"
      ],
      "US": [
       "Experimental development from the late 17th century, practical application from the early 18th century (savery, Newcomen), major efficiency improvements in the late 18th century (Watt), widespread industrial and transportation use throughout the 19th century, declining relevance with electrification and internal combustion in the 20th century.",
       "Developed from late 17th-century precursors (e.g., Savery) through early 18th-century practical designs (e.g., Newcomen) to the highly efficient and versatile engines of the late 18th and 19th centuries (e.g., Watt), with continued significance into the 20th century.",
       "late 17th century to present with key developments in 1800s"
      ],
      "EU": [
       "1712 (Newcomen) to present, with key milestones in 1769 (Watt) and 1825 (Stephenson)",
       "Conceptualized 1st century CE (Heron), prototyped 17th century, industrialized 18th–19th centuries, declined 20th century (replaced by turbines/internal combustion)",
       "1712 (Newcomen) to present, with key milestones in 1769 (Watt), 1814 (Stephenson's locomotive)"
      ]
     },
     "fan": [
      {
       "reading": "Rapid adoption post-Watt (1770s) with no significant pre-industrial use",
       "weight": 0.9,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of widespread pre-Watt industrial steam engine use",
       "followup": "Economic data on pre-1770s energy sources"
      },
      {
       "reading": "18th-20th centuries",
       "weight": 0.85,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "discrepancies in historical timelines",
       "followup": "review of established historical accounts"
      },
      {
       "reading": "Functional origin is late 17th century (Savery/Papin)",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Discovery of a working industrial engine predating 1698",
       "followup": "Deep scan of mining archives pre-1700"
      },
      {
       "reading": "1712-1812",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "proof of steam engine existence before 1712",
       "followup": "examine historical patents and records"
      },
      {
       "reading": "1610-1920s (earlier prototype use)",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "No working steam engines documented before Savery's 1698 patent",
       "followup": "Examine Francis Bacon's 1620 sketches for evidence of steam tech"
      },
      {
       "reading": "16th-20th centuries",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "evidence of limited temporal extent",
       "followup": "research historical engineering advancements"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "accelerated industrial revolution (measured GDP growth, 0.5% avg/yr rise 1780-1840)",
     "enabled global steam-powered transportation (ships/railways)",
     "50%+ reduction in coal consumption for pumping (1780s-1820s)",
     "200%+ industrial output boost (1800-1840)",
     "Enabled the mechanization of industry, driving the Industrial Revolution by powering facto"
    ],
    "aims_by_bloc": {
     "CN": [
      "drain deep coal mines",
      "power textile looms and factories",
      "Powering ships and locomotives (early attempts)",
      "Replacing waterwheels in textile mills"
     ],
     "US": [
      "To efficiently and reliably pump water out of mines and other sub-surface locations.",
      "To provide a universal, portable power source for a wide range of manufacturing processes ",
      "To generate electricity through steam turbines, a later use of steam power principles.",
      "To provide a reliable and powerful source of motive force for industrial machinery, replac"
     ],
     "EU": [
      "Replace human and animal labor in industry",
      "Enable long-distance travel and communication",
      "To replace human/animal/water power with scalable mechanical energy",
      "To demonstrate thermodynamic principles (early experiments)"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 50,
    "end": 1950,
    "markers": [
     50,
     1650,
     1698,
     1712,
     1750,
     1769,
     1776,
     1800,
     1814,
     1825,
     1850,
     1920,
     1950
    ]
   },
   "grounded": {
    "crediting": "neutral",
    "crediting_detail": "Home civ is Greece/Britain (a Western home), so the live external-validity question is whether the CN bloc DEFLATES the Western origin and/or pattern-matches an ancient invention onto China. It does neither. CN qwen states WHERE='England (origin)'; CN deepseek gives the MOST Greece-inclusive accounts of any bloc ('Roman Egypt (Hero's aeolipile)', 'Hero of Alexandria... ancient Alexandria and England'); CN glm credits 'Hellenistic Egypt... UK/Western Europe.' No CN model inven",
    "spine_converges": true,
    "why_complementary": true,
    "ground_truth": "Steam engine has a two-stage origin, confirmed by a multilingual harvest that CONVERGES across English and Chinese-institutional sources. (1) Conceptual/proto origin: the aeolipile, described by Hero (Heron) of Alexandria in 1st-century Roman Egypt (Greek/Hellenistic) — a steam-driven novelty with no practical application. (2) Practical/i",
    "sharp_axes": [
     "what",
     "where",
     "when"
    ],
    "blurred_axes": [
     "who"
    ]
   }
  },
  {
   "id": "A14",
   "title": "paper money (the artefact/instrument, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "various governments, merchants, and financial institutions",
     "agreement": 0.188,
     "sharpness": 0.166,
     "measured_frac": 0.812,
     "perBloc": {
      "CN": [
       "Tang/Song Chinese officials, merchant networks, European bankers, modern central banks",
       "Chinese merchants and imperial governments; later European and global central banks",
       "Song Dynasty officials, Sichuan merchants, Mongol traders, European central banks"
      ],
      "US": [
       "Chinese dynasties, medieval merchants, early modern states, central banks, international financial institutions",
       "governments, banks, traders",
       "various governments, merchants, and financial institutions"
      ],
      "EU": [
       "Multiple cultures (China, Europe, Middle East)",
       "ancient Chinese, medieval Muslims, European bankers, modern central banks",
       "State authorities, merchants, and financial institutions (e.g., Song Dynasty China, European banks, colonial powers)"
      ]
     },
     "fan": [
      {
       "reading": "Developed through cross-cultural exchange",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Clear evidence of a single origin point",
       "followup": "Historical trade and migration records"
      },
      {
       "reading": "Sichuan merchants (as private issuers)",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No merchant records of note issuance survive",
       "followup": "Search Song Dynasty merchant guild archives for draft notes"
      },
      {
       "reading": "Primarily sovereign states exercising power",
       "weight": 0.6,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "A long-lived, successful paper currency system that was never state-issued or controlled.",
       "followup": "Analyze the lifecycle of private banknotes in 19th-century US/Scotland versus state-issued notes."
      },
      {
       "reading": "Song government (state innovation)",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Official Song texts reference private notes as 'counterfeit'",
       "followup": "Analyze Song fiscal records for earliest state-issued note mentions"
      },
      {
       "reading": "Chinese Tang Dynasty officials and salt merchants (7th–9th century)",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier non-Chinese proto-paper money systems",
       "followup": "Archaeological evidence of pre-Tang monetary instruments in other regions"
      },
      {
       "reading": "Primarily commercial networks and merchants",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Archaeological evidence showing the first widespread paper money was issued top-down by a state without pre-existing private precedents.",
       "followup": "Trace the earliest use of 'flying money' in Tang China to confirm its merchant-led origin."
      }
     ]
    },
    "what": {
     "leading": "Paper-based credit instrument representing stored value",
     "agreement": 0.188,
     "sharpness": 0.188,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Paper-based credit instrument representing stored value",
       "Paper promissory notes and fiat currency issued by authorities",
       "Fiat currency notes issued by governments or central banks"
      ],
      "US": [
       "A portable, divisible instrument representing and convertible into specie, issued by an authority and accepted as a medium of exchange and store of value.",
       "paper notes as currency",
       "a negotiable instrument representing value"
      ],
      "EU": [
       "Printed currency made from paper or polymer",
       "printed currency notes representing monetary value",
       "A physical or digital token representing stored value, backed by trust in an issuer (state, bank, or institution), used as a medium of exchange, store of value, and unit of account"
      ]
     },
     "fan": [
      {
       "reading": "Initially made from plant fibers (e.g., mulberry)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of other materials used in early paper money",
       "followup": "Material analysis of ancient paper money"
      },
      {
       "reading": "A debt instrument backed by a commodity (e.g., gold, silver) or state authority",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of paper money functioning without commodity backing",
       "followup": "Historical analysis of fiat vs. commodity-backed systems"
      },
      {
       "reading": "A symbolic representation of trust in an issuing institution",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Collapse of paper money systems despite institutional trust",
       "followup": "Case studies of hyperinflation and monetary crises"
      },
      {
       "reading": "Later versions include synthetic materials (e.g., polymer)",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Historical records of early synthetic paper money",
       "followup": "Manufacturing records from central banks"
      },
      {
       "reading": "Primarily a debt instrument (promissory note) rather than a standalone currency",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of paper money used without debt obligations (e.g., fiat currency)",
       "followup": "Historical records of early paper money transactions without debt repayment"
      },
      {
       "reading": "A tool for state control over economic flows (e.g., taxation, inflation)",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Instances of paper money used outside state control (e.g., private currencies)",
       "followup": "Case studies of non-state paper money systems"
      }
     ]
    },
    "where": {
     "leading": "global, originating in China",
     "agreement": 0.188,
     "sharpness": 0.188,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "China (7th c.), spread to Eurasia via Silk Road, global adoption by 20th c.",
       "Originated in China (7th-11th century), spread to Europe (13th-17th century), then worldwide",
       "Origin: Sichuan, China; Spread: Silk Road, Mongol Empire, Europe, global"
      ],
      "US": [
       "global, originating in China",
       "Originated in Tang/Song Dynasty China; spread globally via trade routes and state adoption to Europe, the Americas, and worldwide financial systems.",
       "originated in China, spread globally"
      ],
      "EU": [
       "Originated in China, spread to Europe, Middle East, and globally",
       "China (7th century), Middle East (10th century), Europe (17th century), global",
       "Originated in Song Dynasty China (10th–13th century), spread to Yuan/Ming China, adopted in medieval Europe (17th century), globalized via colonialism and banking systems (18th–20th century)"
      ]
     },
     "fan": [
      {
       "reading": "First used in Tang Dynasty China (7th century)",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of earlier use in other regions",
       "followup": "Historical records from other civilizations"
      },
      {
       "reading": "First used in Sichuan, China (7th century) for salt trade",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier paper money in Persia or Central Asia",
       "followup": "Archaeological digs in pre-Tang trade hubs"
      },
      {
       "reading": "Primarily China for invention, Europe for systemic iteration and global diffusion model.",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Evidence of parallel, independent development and global spread of paper money concepts originating from other cultural spheres.",
       "followup": "Comparative historical tracing of specific technological and regulatory innovations in paper money across East Asia and Europe."
      },
      {
       "reading": "Adopted in Europe during the 17th century",
       "weight": 0.3,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Earlier European paper money records",
       "followup": "Banking and economic history archives"
      },
      {
       "reading": "Diffusion from China to the Islamic world before Europe",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Absence of Islamic paper money records predating European adoption",
       "followup": "Textual or numismatic evidence of Islamic paper money"
      },
      {
       "reading": "Diffused via Mongol Empire (13th–14th century) to Persia and Europe",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of independent European development of paper money",
       "followup": "Comparative analysis of Mongol and European financial records"
      }
     ]
    },
    "when": {
     "leading": "9th century to present",
     "agreement": 0.312,
     "sharpness": 0.312,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "7th c. Tang Dynasty to present, peak diffusion 12th-14th c. Mongol Era",
       "From 7th century (Tang dynasty) to present",
       "9th–10th c. (Song China); 13th c. (Mongol expansion); 17th c. (European adoption); 20th c. (global standard)"
      ],
      "US": [
       "9th century to present",
       "Proto-forms from Tang Dynasty (c. 7th century CE); widespread use from Song Dynasty (c. 11th century CE); global adoption from post-Renaissance period to present.",
       "started in the 7th century, evolved over centuries"
      ],
      "EU": [
       "7th century to present, with key moments in 7th, 17th, and 20th centuries",
       "7th century CE to present, key moments: 7th c. China, 17th c. Europe, 20th c. global adoption",
       "Temporal extent: 7th–21st century (proto-forms in Tang China, formalization in Song Dynasty, global adoption by 20th century); key moments: 1024 (Song Jiaozi), 1661 (Stockholm Banco), 1971 (Nixon Shock ending gold standard)"
      ]
     },
     "fan": [
      {
       "reading": "First use in Song Dynasty (960-1279)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Song records indicate earlier use",
       "followup": "Analyze historical texts for precursor receipts"
      },
      {
       "reading": "First widespread use in 7th century China",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Earlier use in other regions",
       "followup": "Archaeological and historical records"
      },
      {
       "reading": "First proto-paper money in Tang China (618–907 CE) as 'flying money'",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier paper-based monetary instruments",
       "followup": "Analysis of Tang Dynasty financial records"
      },
      {
       "reading": "First use in Tang Dynasty (618-907)",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "No surviving Tang paper money",
       "followup": "Search for archeological evidence of early banknotes"
      },
      {
       "reading": "Modern paper money standardized in 20th century",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Earlier standardization efforts",
       "followup": "Central bank records and economic history"
      },
      {
       "reading": "Earlier proto-paper money in Tang China (7th–9th century) as direct precursor",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of surviving Tang-era paper money artifacts",
       "followup": "Discovery of Tang-era promissory notes or receipts"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Led to inflation when overissued",
     "Increased velocity and scale of trade",
     "Facilitated Song Dynasty state tax collection",
     "Enabled large-scale trade and economic growth",
     "Facilitated greater scale and speed of commerce, enabled state finance (taxation, war fund"
    ],
    "aims_by_bloc": {
     "CN": [
      "Facilitate commerce and government finance",
      "Monetize national economies",
      "Fund state military expenditures",
      "To create a stable medium of exchange"
     ],
     "US": [
      "facilitate international trade",
      "control inflation",
      "enable government financing",
      "promote economic growth"
     ],
     "EU": [
      "Replace commodity money (e.g., gold, silver)",
      "Enable centralized monetary control",
      "stabilize economies through monetary policy",
      "reduce reliance on precious metals"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 650,
    "end": 2050,
    "markers": [
     650,
     850,
     950,
     1024,
     1050,
     1250,
     1350,
     1650,
     1661,
     1950,
     1971,
     2050
    ]
   },
   "grounded": {
    "crediting": "neutral",
    "crediting_detail": "China is both home civ and true origin, so the test is whether non-CN blocs erase or relocate the Chinese origin. They do not: all US models (gemini, gpt4omini, llama) and both EU models (mistral, mistral-lg) state origin as China Tang/Song; none substitute Europe (Stockholms Banco/Palmstruch) as origin, so no Western re-crediting. CN models keep the European/global diffusion phase, no over-reach. Two minor non-home distortions: one EU mistral entry adds the Islamic Middle Ea",
    "spine_converges": true,
    "why_complementary": true,
    "ground_truth": "Origin: CHINA. Tang flying cash (feiqian, 7th-9th c.) was a remittance draft, NOT true circulating money. First true circulating paper currency: jiaozi, private notes in Chengdu, Sichuan, Northern Song (late 10th/early 11th c.), state-issued via Jiaozi wu in 1023; driven by heavy iron coinage in Sichuan. Diffused west via Mongol/Yuan era;",
    "sharp_axes": [
     "where",
     "when"
    ],
    "blurred_axes": [
     "who"
    ]
   }
  },
  {
   "id": "A15",
   "title": "the seismometer (the instrument/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Luigi Palmieri, John Milne, Emil Wiechert, modern seismologists",
     "agreement": 0.25,
     "sharpness": 0.212,
     "measured_frac": 0.75,
     "perBloc": {
      "CN": [
       "John Milne, Andrey Sacharov, global seismic networks",
       "Zhang Heng (original) + Western scientists (refinement)",
       "A global fan of physicists, geologists, and engineers, from Zhang Heng to Milne, Benioff, and modern network operators"
      ],
      "US": [
       "Early scientific pioneers (e.g., Mallet, Milne), instrument engineers, global seismological institutions and networks, geophysicists, and military intelligence analysts.",
       "A lineage of pioneers, theorists, institutional builders, and global user communities.",
       "scientists, engineers, geophysicists"
      ],
      "EU": [
       "Luigi Palmieri, John Milne, Emil Wiechert, modern seismologists",
       "Luigi Palmieri, John Milne, Ernst von Reyer, modern seismologists",
       "Chinese polymaths (Han dynasty), European natural philosophers (18th-19th c.), modern geophysicists"
      ]
     },
     "fan": [
      {
       "reading": "Chinese scholars (via Buddhist transmission)",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No documented seismic texts in early Indian Buddhist sutras",
       "followup": "Examine 7th-10th c. Chinese Buddhist translation records for seismic references"
      },
      {
       "reading": "The academic scientific community",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Historical records showing military or commercial entities as the primary drivers of all major innovations.",
       "followup": "Analyze funding sources and institutional affiliations of key innovators across history."
      },
      {
       "reading": "Seismology community",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "no community involvement",
       "followup": "interviews with experts"
      },
      {
       "reading": "Independent parallel development in China and Europe",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Documented transmission of Chinese seismographic knowledge to Europe before 18th c.",
       "followup": "Analysis of medieval Arabic or Persian texts for seismographic references"
      },
      {
       "reading": "Modern researchers",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Absence of contemporary publications",
       "followup": "Review recent scientific literature on seismometer advancements"
      },
      {
       "reading": "Direct Chinese-to-Italian transmission (17th c.)",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No Italian scientists cite Chinese sources in 1600s seismometer texts",
       "followup": "Search 1600-1800s Italian scientific correspondence for Chinese instrument references"
      }
     ]
    },
    "what": {
     "leading": "ground motion detection instrument",
     "agreement": 0.312,
     "sharpness": 0.312,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "ground motion detection instrument",
       "measures ground motion via mechanical/electronic transduction",
       "An instrument that detects and records ground motion (seismic waves)"
      ],
      "US": [
       "A device for detecting, recording, and analyzing ground motion, primarily seismic waves generated by earthquakes or artificial sources.",
       "An instrument designed to detect, measure, and record ground motion, evolving from mechanical to sensitive electronic and digital systems.",
       "sensitive instrument for detecting ground motion"
      ],
      "EU": [
       "Instrument to detect and measure seismic waves (earthquakes, volcanic activity)",
       "Instrument detecting and recording ground motion (seismic waves) via mechanical, optical, or electronic transduction",
       "Instrument detecting and recording ground motion (seismic waves) via mechanical, electromagnetic, or digital means"
      ]
     },
     "fan": [
      {
       "reading": "seismic wave recorder",
       "weight": 0.9,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "no seismic wave recording capability",
       "followup": "device testing"
      },
      {
       "reading": "Multi-modal sensor integrating mechanical, electromagnetic, and digital components",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of modern seismometers lacking digital components",
       "followup": "Survey of contemporary seismometer designs and patents"
      },
      {
       "reading": "Purely mechanical device (e.g., Zhang Heng's urn)",
       "weight": 0.3,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of pre-modern electronic or optical components in seismometers",
       "followup": "Material analysis of surviving ancient seismometers"
      },
      {
       "reading": "analog and digital systems for seismic measurement",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "irrelevance to seismic data collection",
       "followup": "technical specifications of various models"
      },
      {
       "reading": "vibration detector",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "no vibration detection capability",
       "followup": "device inspection"
      },
      {
       "reading": "Early forms may have been purely observational (e.g., water-filled vessels)",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "No physical evidence of pre-mechanical seismometers",
       "followup": "Analysis of ancient Chinese texts for non-mechanical seismic detection methods"
      }
     ]
    },
    "where": {
     "leading": "Originated in Italy (1855), spread globally (Europe, Japan, US, etc.)",
     "agreement": 0.188,
     "sharpness": 0.166,
     "measured_frac": 0.812,
     "perBloc": {
      "CN": [
       "Japan (1880s), global seismic stations",
       "China (1st-2nd c.) → Japan (17th c.) → Europe (19th c.)",
       "Originated in Han Dynasty China, later in Europe, now globally distributed"
      ],
      "US": [
       "Originating in 19th-century Europe (e.g., Italy, UK), now globally distributed in scientific observatories, research institutions, disaster monitoring centers, and exploration missions.",
       "Originated in 19th-century Europe (UK, Italy) and Japan; now global, integrated into scientific networks and research centers worldwide.",
       "global distribution, originating in Europe"
      ],
      "EU": [
       "Originated in Italy (1855), spread globally (Europe, Japan, US, etc.)",
       "Originated in Italy (1855), spread globally (Europe, Americas, Asia)",
       "Originated in China (Han dynasty), refined in Europe (18th-19th c.), globalized via seismic networks (20th c. onward)"
      ]
     },
     "fan": [
      {
       "reading": "Widespread use in earthquake-prone areas",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Absence of disaster response initiatives",
       "followup": "Review emergency response plans and protocols"
      },
      {
       "reading": "Primarily a Chinese and European invention",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Evidence of a sophisticated, independent precursor in another region (e.g., the Americas).",
       "followup": "Conduct a comparative archaeological and historical analysis of early motion-sensing devices globally."
      },
      {
       "reading": "A convergent global effort with no single origin point",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Clear, unambiguous historical lines showing a single point of origin for all subsequent development.",
       "followup": "Map the intellectual and technological lineage of all key seismometer designs to identify root concepts."
      },
      {
       "reading": "Europe and North America",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "no evidence of use in these regions",
       "followup": "historical records review"
      },
      {
       "reading": "Exclusively Chinese origin with later European reinvention",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Archaeological evidence of seismometers in pre-Han China or contemporaneous cultures",
       "followup": "Cross-cultural comparison of ancient scientific instruments"
      },
      {
       "reading": "Limited to research institutions",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Evidence of widespread adoption",
       "followup": "Conduct surveys of seismometer users"
      }
     ]
    },
    "when": {
     "leading": "19th century to present",
     "agreement": 0.25,
     "sharpness": 0.241,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "1880s-present, key: 1930s (electronic), 1970s (digital)",
       "1st c. AD (Chinese predecessors) to present",
       "c. 132 CE to present, with key refinements in the 18th-20th centuries"
      ],
      "US": [
       "19th century to present",
       "Conceptual development from the mid-19th century, with key advances in analog recording through the early 20th century, and transition to digital and broadband seismology from the mid-20th century to the present.",
       "First significant prototypes emerged mid-19th century; continuous development and widespread adoption through the 20th century, becoming indispensable in the late 20th/early 21st century with digital networks."
      ],
      "EU": [
       "1855 (first modern seismometer) to present, with key milestones (1900s: electromagnetic, 1960s: digital)",
       "1855 (first modern seismometer) to present, with key refinements in 20th-21st centuries",
       "~132 CE (Han dynasty) to present, with key moments: 18th c. European revival, 1880s (Milne's horizontal pendulum), 1960s (digital seismometry)"
      ]
     },
     "fan": [
      {
       "reading": "2nd c. AD origin (Zhang Heng)",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Zhang Heng's 132 AD seismoscope described but no physical artifact found",
       "followup": "Archaeological survey of Han dynasty sites for possible seismoscope fragments"
      },
      {
       "reading": "19th century to present",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "no evidence of use in 19th century",
       "followup": "device inspection"
      },
      {
       "reading": "Discontinuous existence (lost between Han and 18th c.)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of post-Han, pre-18th c. seismometers",
       "followup": "Archival research in Byzantine, Islamic, or medieval European texts"
      },
      {
       "reading": "Continuous refinement with incremental improvements",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of abrupt technological regressions or gaps",
       "followup": "Technical comparison of seismometers across centuries"
      },
      {
       "reading": "Late 1st c. BC origin (pre-Zhang)",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No pre-Han Chinese texts reference earthquake detection devices",
       "followup": "Examine bamboo slip records from Warring States period"
      },
      {
       "reading": "20th century only",
       "weight": 0.2,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "evidence of earlier use",
       "followup": "historical records review"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "reduced earthquake fatalities via early warning",
     "scientific understanding of Earth's interior",
     "Earthquake early warning systems",
     "Plate tectonics validation",
     "Accurate mapping of Earth's internal structure (crust, mantle, core) and seismic wave prop"
    ],
    "aims_by_bloc": {
     "CN": [
      "precise earthquake prediction",
      "quantitative seismic hazard mapping",
      "Earthquake prediction",
      "Geological surveying"
     ],
     "US": [
      "To gain insight into earthquake prediction through identifying precursor signals and under",
      "To map subterranean geological formations for resource exploration (e.g., mineral deposits",
      "To monitor volcanic processes to prevent or mitigate eruptions.",
      "To accurately locate earthquake epicenters and determine their magnitudes."
     ],
     "EU": [
      "Predict earthquakes with high accuracy",
      "Monitor nuclear tests and underground explosions",
      "Study Earth's internal structure",
      "Predict earthquakes (unrealized)"
     ]
    },
    "complementarity": 0.974
   },
   "when_span": {
    "start": 50,
    "end": 2050,
    "markers": [
     50,
     150,
     1750,
     1850,
     1855,
     1880,
     1950,
     2050
    ]
   },
   "grounded": {
    "crediting": "under_credits_others",
    "crediting_detail": "The home civ here is CHINA, and the crediting failure runs the OTHER way from the usual home-bias worry: the non-home (US + EU) blocs systematically UNDER-credit China. Of the US bloc, every sample (gemini x2, gpt4omini x2, llama x2) OMITS Zhang Heng and dates the origin to '19th-century Europe' or 'global/worldwide' — gemini explicitly says 'originated in 19th-century Europe (Italy, UK) and Japan'. EU's mistral (x2) also omits Zhang Heng and sets origin = 'Italy 1855'. So 8 ",
    "spine_converges": false,
    "why_complementary": true,
    "ground_truth": "Seismoscope (the originating artefact): Zhang Heng (张衡), 132 CE, Han Dynasty China, capital Luoyang (Luoyang/Loyang) — the Houfeng Didong Yi (候风地动仪), a bronze urn ~2m wide with 8 dragon-heads/balls and an internal pendulum (du-zhu). It is a SEISMOSCOPE / 验震器 — it detects and indicates the direction of a distant quake; it does NOT continuo",
    "sharp_axes": [
     "when (terminus): all blocs agree the instrument runs to the present / is globally distributed",
     "what: all blocs converge on 'instrument that detects/records ground motion (seismic waves)' — qualitatively identical across CN/US/EU",
     "modern-refinement chain (where the models name it): Italy (Palmieri/Cecchi) and Japan (Milne 1880) are correctly and consistently identified by every bloc that reaches the 19th century — this part of the spine DOES converge and matches harvest"
    ],
    "blurred_axes": [
     "where (origin): CN+mistral-lg say China/Han Luoyang (correct); US (gemini/gpt4omini/llama) + mistral say Europe/Italy/global — a hard bloc split off the harvested truth",
     "when (start date): splits between 132 CE (CN, mistral-lg — correct) and 1850s/19th c. (US, mistral — truncated, drops the Chinese origin by ~1700 yrs)",
     "who (originator): Zhang Heng named by CN + mistral-lg; absent from all US samples and from mistral — the single most divergent axis",
     "device-type (seismoscope vs seismometer): the harvest's key nuance — Zhang Heng's is a seismoscope, not a true seismometer — is collapsed by ALL blocs; none distinguishes detection-only from continuous-recording, so the '132 CE first seismometer' claim is itself an over-flattening even where China is credited"
    ]
   }
  },
  {
   "id": "A2",
   "title": "gunpowder (the substance/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Chinese alchemists, military engineers, European scientists",
     "agreement": 0.438,
     "sharpness": 0.355,
     "measured_frac": 0.688,
     "perBloc": {
      "CN": [
       "Chinese alchemists",
       "Chinese alchemists (c. 9th century) and subsequent global adopters",
       "Chinese alchemists, Arabic chemists, European gunners"
      ],
      "US": [
       "Alchemists and military leaders",
       "Alchemists, military engineers, miners, and pyrotechnicians across civilizations",
       "A lineage of Chinese alchemists, Arab intermediaries, Mongol conquerors, European military powers, and global industrial societies."
      ],
      "EU": [
       "Chinese alchemists, European military engineers, global industrialists",
       "Chinese alchemists (originators), Song Dynasty military engineers (refiners), Mongol transmitters, European and Islamic military technologists (adopters and developers)",
       "Chinese alchemists, European chemists, military strategists"
      ]
     },
     "fan": [
      {
       "reading": "Ancient Chinese scholars, driven by alchemical pursuits for elixir of immortality",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Discovery of explicit textual evidence indicating gunpowder's origin was purely secular or military.",
       "followup": "Detailed textual and archaeological analysis of earliest Chinese alchemical manuscripts and production sites."
      },
      {
       "reading": "Developed by Song dynasty military engineers (c. 10th-11th century) for fireworks and weapons",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Earlier evidence of gunpowder in Dunhuang manuscripts (c. 850) contradicts late origin",
       "followup": "Radiocarbon dating of early gunpowder residues from archaeological sites"
      },
      {
       "reading": "Chinese alchemists",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Lack of historical records",
       "followup": "Research on ancient Chinese texts"
      },
      {
       "reading": "Invented by Sun Simiao (c. 650 CE) in Daoist alchemy",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Lack of contemporary records linking Sun to gunpowder",
       "followup": "Examine Tang dynasty alchemical texts for explicit gunpowder recipe"
      },
      {
       "reading": "The Mongol Empire's military campaigns",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Lack of contemporary Mongol battlefield evidence for gunpowder use contemporaneous with its rapid spread.",
       "followup": "Cross-referencing battlefield reports from various regions with Mongol army movements and material procurement records."
      },
      {
       "reading": "Only Chinese alchemists and military engineers",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence of early European formulations and applications",
       "followup": "Historical accounts of European adoption"
      }
     ]
    },
    "what": {
     "leading": "Potassium nitrate, charcoal, sulfur mixture",
     "agreement": 0.75,
     "sharpness": 0.75,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Potassium nitrate, charcoal, sulfur mixture",
       "Combustible mixture of saltpeter (KNO3), sulfur, and charcoal, used as propellant and explosive",
       "A mixture of saltpeter (potassium nitrate), sulfur, and charcoal, which deflagrates rapidly producing hot gas"
      ],
      "US": [
       "A flammable, explosive chemical mixture primarily of sulfur, charcoal, and a nitrate oxidizer (historically potassium nitrate)",
       "A pyrotechnic composition, primarily black powder (saltpeter, charcoal, sulfur), capable of rapid deflagration and propellant force.",
       "Chemical mixture primarily of potassium nitrate, sulfur, and charcoal"
      ],
      "EU": [
       "Explosive mixture of saltpeter, sulfur, and charcoal",
       "A low-explosive mixture of saltpeter (potassium nitrate), sulfur, and charcoal, used for propulsion, pyrotechnics, and weaponry",
       "A low-explosive mixture of saltpeter (potassium nitrate), sulfur, and charcoal, used for propulsion, pyrotechnics, and warfare"
      ]
     },
     "fan": [
      {
       "reading": "primarily a propellant",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "demonstrations of explosive properties in controlled environments",
       "followup": "laboratory experiments on decomposition and reaction rates"
      },
      {
       "reading": "Originally a medicinal or elixir compound, not an explosive",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Alchemical texts describing gunpowder as a medicine with no explosive properties",
       "followup": "Analysis of early alchemical recipes for gunpowder precursors"
      },
      {
       "reading": "mainly used for fireworks",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "historical records of its use in warfare",
       "followup": "analysis of manufacturing records for different uses"
      },
      {
       "reading": "A byproduct of saltpeter purification processes, not intentionally formulated",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Texts describing deliberate mixing of ingredients for explosive purposes",
       "followup": "Study of saltpeter production methods in Tang/Song China"
      },
      {
       "reading": "Variant mixtures",
       "weight": 0.1,
       "tag": "modelled",
       "bloc": "US",
       "falsifier": "Chemical analysis of historical gunpowder samples",
       "followup": "Experimentation with different mixture ratios"
      },
      {
       "reading": "Pyrotechnic composition with variable ratios",
       "weight": 0.05,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Consistent historical recipes across cultures",
       "followup": "Analyze historical gunpowder samples for composition"
      }
     ]
    },
    "where": {
     "leading": "Originated in China, spread to Middle East, Europe, and globally",
     "agreement": 0.562,
     "sharpness": 0.478,
     "measured_frac": 0.75,
     "perBloc": {
      "CN": [
       "East Asia (China) origin",
       "East Asia (China) to global diffusion",
       "Originated in China (Tang/Song dynasties), spread via Silk Road to Islamic world and Europe, then globally"
      ],
      "US": [
       "Originated in ancient China (Tang Dynasty likely), spreading via the Silk Road and Mongol conquests to the Middle East, Europe, and globally",
       "Originated in Imperial China, disseminated east and west across Eurasia via trade routes, military conquest, and scholarly transmission, becoming a global technology.",
       "Originated in China, spread to Europe, the Middle East, and beyond"
      ],
      "EU": [
       "Originated in China, spread to Middle East, Europe, and globally",
       "Originated in China (9th century), spread via Mongol conquests to Islamic world (13th century), then Europe (14th century), and globally via colonialism (16th century onward)",
       "Originated in China (Tang/Song Dynasties), spread via Silk Road to Islamic world, Europe, and globally; key loci include China, Middle East, Europe, and colonial territories"
      ]
     },
     "fan": [
      {
       "reading": "Only spread through the Silk Road",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence of independent discovery in Europe",
       "followup": "Examine trade routes and historical records of diffusion"
      },
      {
       "reading": "Evolved primarily in military contexts",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Usage in mining and fireworks",
       "followup": "Investigate diverse applications throughout different eras"
      },
      {
       "reading": "Originated in China",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Lack of Chinese historical records",
       "followup": "Research on Chinese historical documents"
      },
      {
       "reading": "Primarily diffused by Islamic alchemists and technologists during the medieval period.",
       "weight": 0.3,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Evidence suggesting direct transmission from Chinese military to non-Islamic cultures or parallel, independent development.",
       "followup": "Tracing specific chemical notations and experimental practices from China to the Islamic world and beyond."
      },
      {
       "reading": "Developed in Middle East and Europe",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "No archaeological evidence",
       "followup": "Excavations in Middle Eastern and European historical sites"
      },
      {
       "reading": "Spread to Europe via Mongol conquests, not Silk Road trade",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "European texts describing gunpowder before 13th century Mongol contacts",
       "followup": "Analysis of Mongol-era trade and military records"
      }
     ]
    },
    "when": {
     "leading": "9th century CE to present",
     "agreement": 0.5,
     "sharpness": 0.5,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "9th century CE to present",
       "9th CE (China) to present",
       "c. 850 CE to present; key milestones: first recipes in Chinese texts (c. 850), use in firearms (12th c.), European adoption (13th-14th c.), industrial use (19th c.)"
      ],
      "US": [
       "First empirical evidence, likely accidental, by 9th century in China (Tang Dynasty); chemical formula by 11th century; widespread military adoption by 13th-14th centuries in Eurasia; continuous refinement and application thereafter worldwide.",
       "Evolving from alchemical experimentation in Tang Dynasty China (c. 9th century CE) to widespread military application by the Song Dynasty, rapid Eurasian dissemination during the Mongol era, and transformative military-industrial impact in Europe by the Renaissance and beyond.",
       "First recorded use around 9th century AD, with significant developments in the 13th century"
      ],
      "EU": [
       "9th century CE to present, with key developments in 12th-15th centuries",
       "First documented in China (9th century), refined for military use (10th-12th centuries), spread to Islamic world (13th century), Europe (14th century), and globalized by 16th century; key moments include Song Dynasty fire-lance (10th c.), Mongol cannon (13th c.), and European artillery (15th c.)",
       "9th century CE to present, with key developments in 13th-15th centuries"
      ]
     },
     "fan": [
      {
       "reading": "Its peak use was during the 17th century",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence of continued significant military use afterward",
       "followup": "Assess military records through the 18th and 19th centuries"
      },
      {
       "reading": "Tang Dynasty (9th Century)",
       "weight": 0.7,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Carbon dating of residue on artifacts predating 850 AD showing later composition",
       "followup": "Chemical analysis of early 'fire drug' artifacts"
      },
      {
       "reading": "Invented in 9th century China",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Lack of historical records",
       "followup": "Research on ancient Chinese texts"
      },
      {
       "reading": "Key development occurred during the Song Dynasty's defensive needs against northern incursions.",
       "weight": 0.3,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Archival material indicating similar or greater impetus for development from intellectual curiosity or other non-military drivers.",
       "followup": "Review of Song Dynasty military chronicles and alchemical treatises for explicit links between defensive pressure and gunpowder innovation."
      },
      {
       "reading": "It was first documented in the 8th century",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Earlier evidence is found post-8th century",
       "followup": "Research older texts and artifacts"
      },
      {
       "reading": "Developed in 13th century Europe",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "No documented experiments",
       "followup": "Analysis of European historical manuscripts"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Revolutionized warfare through firearms/rockets",
     "Revolutionized artillery and warfare",
     "Revolutionized warfare through development of firearms, cannons, and explosive devices.",
     "Enabled large-scale mining and construction through controlled explosive demolition.",
     "Facilitated development of pyrotechnics and signaling systems."
    ],
    "aims_by_bloc": {
     "CN": [
      "Militarization of empires",
      "Pyrotechnic entertainment",
      "Military conquest and siege warfare",
      "Military dominance (cannons, muskets, bombs)"
     ],
     "US": [
      "Military conquest",
      "Mining and construction",
      "Seeking immortality or medicinal compounds",
      "Developing more effective incendiary weapons or fireworks"
     ],
     "EU": [
      "Achieve immortality through alchemy",
      "Create more effective weapons",
      "Used for pyrotechnics (festivals, signaling) in China and Europe",
      "Employed as a tool for state control (e.g., Ottoman janissaries, European standing armies)"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 850,
    "end": 1850,
    "markers": [
     850,
     950,
     1050,
     1150,
     1250,
     1350,
     1450,
     1550,
     1850
    ]
   },
   "grounded": {
    "crediting": "under_credits_others",
    "crediting_detail": "China is the sole true origin so over-crediting home is impossible; no bloc Europeanizes gunpowder. Under-credited node = the Islamic/Arab intermediary, dropped by qwen-CN, the gpt4omini-US pair, llama-US and mistral-EU; credited by deepseek-CN, gemini-US, gpt4omini, mistral-EU and both mistral-lg-EU. Soft Western under-crediting of the non-home relay, not home over-crediting.",
    "spine_converges": true,
    "why_complementary": true,
    "ground_truth": "CHINA, single origin. saltpeter KNO3 + sulfur + charcoal. Proto-formula Tang 808 CE (Sun Simiao); first military formula Wujing Zongyao 1044; weapons 904-1298. West via Mongols to Islamic world (Hasan al-Rammah ~1240s) then Europe (Roger Bacon 1267). No non-Chinese precursor. Sources: en.wikipedia History_of_gunpowder, afe.easia.columbia.",
    "sharp_axes": [
     "what",
     "where",
     "when"
    ],
    "blurred_axes": [
     "who",
     "why"
    ]
   }
  },
  {
   "id": "A3",
   "title": "paper (the material/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Chinese papermakers, Cai Lun, Islamic refiners, European millers",
     "agreement": 0.188,
     "sharpness": 0.166,
     "measured_frac": 0.812,
     "perBloc": {
      "CN": [
       "Chinese papermakers, Cai Lun, Islamic refiners, European millers",
       "Cai Lun (China), then Arab papermakers (e.g., Samarra), European workshops (e.g., Fabriano, Venice)",
       "Han dynasty Chinese (Cai Lun), Arab papermakers (Baghdad), European millers (Fabriano)"
      ],
      "US": [
       "A dynamic global network of artisans, scholars, merchants, and inventors involved in its production, refinement, transmission, and application.",
       "Humanity, notably Chinese artisans, Islamic scholars, European printers, and global industries",
       "East Asian cultures, European traders, and modern manufacturers"
      ],
      "EU": [
       "Ancient Egyptians (originators), Chinese (refiners), Islamic world (transmitters), Europeans (mass adopters), global users (modern)",
       "Ancient Egyptians (Papyrus makers), Han Chinese (true paper), Islamic world (transmission), European medieval scribes, industrial papermakers (19th century)",
       "Cai Lun (China), Egyptians, Arabs, Europeans"
      ]
     },
     "fan": [
      {
       "reading": "Gradual development by multiple anonymous craftsmen over centuries",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Evidence of a single coherent invention event with clear predecessor would refute gradual development",
       "followup": "Comparative analysis of fiber composition and sheet formation techniques across early sites"
      },
      {
       "reading": "Banu Musa brothers (8th-9th century Baghdad)",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No surviving documents or archaeological evidence attributing papermaking to them",
       "followup": "Analyze Abbasid-era manuscripts for production marks or factory records"
      },
      {
       "reading": "Indigenous Chinese invention (Cai Lun, 105 CE), no prior Egyptian influence",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Discovered 500 BCE Egyptian papyrus-based writing surface",
       "followup": "Archaeological analysis of pre-105 CE Chinese artifacts"
      },
      {
       "reading": "Cai Lun (Han Eunuch) as primary inventor",
       "weight": 0.6,
       "tag": "historical_record",
       "bloc": "CN",
       "falsifier": "Discovery of paper fragments reliably dated before 105 CE",
       "followup": "Carbon-dating analysis of early Han dynasty archaeological fragments"
      },
      {
       "reading": "Anonymous Chinese artisans before Cai Lun (c. 2nd century BCE)",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Discovery of paper samples clearly pre-dating Cai Lun but not using his method",
       "followup": "Radiocarbon dating of early paper fragments from Dunhuang and other sites"
      },
      {
       "reading": "Cai Lun as sole inventor in 105 CE",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Discovery of pre-Cai Lun paper fragments would refute sole invention",
       "followup": "Radiocarbon dating of early paper samples from Dunhuang or Fangmatan"
      }
     ]
    },
    "what": {
     "leading": "Sheet material made from plant cellulose fibers, used for writing, printing, wrapping",
     "agreement": 0.375,
     "sharpness": 0.375,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Sheet material made from plant cellulose fibers, used for writing, printing, wrapping",
       "Plant-based fibrous sheet (wood pulp, hemp, linen rags)",
       "cellulose fiber sheets bonded into flexible writing surface"
      ],
      "US": [
       "A flexible, thin sheet material made by mechanically and/or chemically processing cellulose fibers derived from wood, rags, grasses, or other vegetable sources, formed into a continuous web.",
       "A thin sheet material made primarily from macerated cellulose fibers, used as a surface for writing, printing, packaging, and fabrication.",
       "a biodegradable material for writing and printing"
      ],
      "EU": [
       "Cellulose-based writing/printing substrate, flexible, durable, and mass-producible",
       "A thin, flexible sheet material made from plant fibers (cellulose), used for writing, packaging, and construction, with properties of absorbency, durability, and low cost",
       "Thin, flexible material made from plant fibers, used for writing and packaging"
      ]
     },
     "fan": [
      {
       "reading": "Primarily a medium for symbolic communication (writing/art)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of paper used predominantly for non-symbolic purposes (e.g., early packaging)",
       "followup": "Analyze earliest surviving paper fragments for functional traces"
      },
      {
       "reading": "Primarily a medium for written communication and art",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Archaeological discovery of non-writing uses dominating early contexts would refute primary function",
       "followup": "Examine earliest paper artifacts for ink residues, folding patterns, and reuse"
      },
      {
       "reading": "Originally a wrapping/padding material later adapted for writing",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Early written documents on paper precede any wrapping finds by centuries",
       "followup": "Systematic survey of pre-2nd century CE paper fragments for absence of ink"
      },
      {
       "reading": "A fragile substrate for ephemeral or durable communication and data storage.",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Discovery of inherently durable paper types or treatments that make it immune to degradation under all conditions.",
       "followup": "Long-term environmental stability testing of various paper compositions and archival storage methods."
      },
      {
       "reading": "Thin sheet of rag fibers (cotton, linen) primarily",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Widespread use of wood pulp paper in modern times contradicts exclusive rag fiber origin",
       "followup": "Historical analysis of fiber sources in different eras"
      },
      {
       "reading": "Paper as a generic term includes papyrus-like materials",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Papyrus is made from sliced reeds, not pulped fibers; distinct from paper",
       "followup": "Clarify definition in historical contexts"
      }
     ]
    },
    "where": {
     "leading": "Originated in Han Dynasty China (2nd century BCE–1st century CE), spread to Islamic world (8th c.), Europe (12th c.), global (19th c.)",
     "agreement": 0.312,
     "sharpness": 0.301,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "Originated in Han Dynasty China (2nd century BCE–1st century CE), spread to Islamic world (8th c.), Europe (12th c.), global (19th c.)",
       "Origin: Yangling (China); Spread: Middle East (751 CE), Europe (12th-13th c.), then global",
       "China (Yangzhou, 2nd c. CE), Baghdad (8th c.), Fabriano (13th c. Europe)"
      ],
      "US": [
       "Originated in Han Dynasty China, disseminated globally through trade routes via the Middle East and Central Asia, becoming a ubiquitous material worldwide.",
       "Originated in ancient China; spread via Silk Road and Islamic world to Europe, then globally",
       "China, spreading to Asia and Europe"
      ],
      "EU": [
       "Originated in China, spread to Middle East, Europe, and globally",
       "Originated in China (Han Dynasty), spread via Silk Road to Islamic world, then Europe, now global",
       "Originated in Han China (2nd century BCE), spread via Silk Road to Islamic world (8th century CE), then Europe (12th century CE), globalized by colonialism/industrialization (19th century)"
      ]
     },
     "fan": [
      {
       "reading": "Spread via Silk Road and Arab trade networks",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "No historical records of paper in those regions",
       "followup": "Examine trade records and archaeological finds"
      },
      {
       "reading": "Sogdian Silk Road hubs (central Asia) as key diffusion point",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No papermaking artifacts found in Sogdian sites pre-751 CE",
       "followup": "Archaeological survey of Bukhara and Samarkand for pre-751 paper residues"
      },
      {
       "reading": "Direct Chinese → Abbasid transmission via Silk Road",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No papermaking relics in Central Asian trade hubs",
       "followup": "Carbon-dating of paper artifacts along Silk Road routes"
      },
      {
       "reading": "Independent origins in Egypt (papyrus) and China (paper) with no direct linkage",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of shared tools or fiber sources between papyrus and paper",
       "followup": "Compare microscopic fiber structures and processing tools"
      },
      {
       "reading": "Centres of knowledge propagation, particularly within monastic and academic institutions.",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence of paper's widespread use and production in areas historically disconnected from major knowledge centres.",
       "followup": "Mapping of historical paper mills and distribution networks against centres of learning and administration."
      },
      {
       "reading": "originated in Asia",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "evidence of independent development elsewhere",
       "followup": "genetic analysis of plants"
      }
     ]
    },
    "when": {
     "leading": "from 2nd century CE to present",
     "agreement": 0.188,
     "sharpness": 0.18,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "From at least 2nd century BCE to present, with critical epochs: 105 CE (Cai Lun), 8th c. (Islamic adoption), 13th c. (European mills), 19th c. (wood pulp paper)",
       "105 CE (China) - present; Key: 751 CE (Arab adoption), 12th c. (Europe), 15th c. (printing press integration)",
       "2nd c. CE (invention) → 13th c. (European adoption) → 19th c. (industrialization)"
      ],
      "US": [
       "Its history spans from its earliest documented invention in Imperial China (c. 105 CE) through continuous evolution, global adoption, and industrialization to the present day.",
       "From its invention circa 1st-2nd century CE in China, through global adoption and innovation, to its sustained, though evolving, use in the 21st century.",
       "2nd century AD to present, with key moments in the 11th and 15th centuries"
      ],
      "EU": [
       "Invented ~2nd century BCE (China), refined ~8th century CE (Islamic world), industrialized ~19th century (Europe), digital decline ~21st century",
       "Invented ~200 BCE (Han China), refined 105 CE (Cai Lun), spread to Islamic world by 800 CE, Europe by 1100 CE, mechanized 1800s, digital decline 2000s",
       "Invented ~2nd century BCE, widespread by 10th century CE, modern forms 19th century CE"
      ]
     },
     "fan": [
      {
       "reading": "Continuous evolution from earlier fabric and bark cloth, no single 'invention' date",
       "weight": 0.7,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Clear break in technology (e.g., sudden appearance of beaten fiber sheets) would refute continuity",
       "followup": "Trace morphological changes in fiber processing from bark cloth to early paper in China"
      },
      {
       "reading": "The primary medium for the Information Revolution, peaking from the Gutenberg press to the digital age.",
       "weight": 0.7,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Evidence showing paper's impact was demonstrably less significant or influential during this era compared to earlier or later periods.",
       "followup": "Analysis of text production volume, literacy rates, and knowledge dissemination velocity across historical periods."
      },
      {
       "reading": "12th century as primary European adoption (post-1150 CE)",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Pre-12th-century European paper fragments found in Spain (e.g., Silos Abbey, 1125 CE)",
       "followup": "Carbon dating of surviving early European paper fragments"
      },
      {
       "reading": "Paper was not widely used until the 2nd century CE",
       "weight": 0.7,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Discovery of a large corpus of paper documents from earlier centuries",
       "followup": "Large-scale archaeological surveys in Han dynasty sites"
      },
      {
       "reading": "Invention 105 CE (Cai Lun), first European mill 1150 (Xàtiva)",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No Han dynasty paper records before 105 CE",
       "followup": "Examination of fragmented Ban Chao documents (c. 80-100 CE)"
      },
      {
       "reading": "Invention date c. 105 CE",
       "weight": 0.5,
       "tag": "documented",
       "bloc": "CN",
       "falsifier": "Discovery of uncontested paper evidence pre-dating 105 CE",
       "followup": "Re-evaluation of tomb inventories from Western Han period"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Enabled mass literacy, bureaucracy, printing, and scientific record-keeping",
     "Revolutionized packaging, hygiene (toilet paper), and currency (banknotes)",
     "Accelerated the dissemination of knowledge, facilitated mass literacy and education, enabl",
     "Revolutionized information storage and dissemination, enabling mass literacy, state admini",
     "Facilitated the development of new legal, economic, and governance structures through stan"
    ],
    "aims_by_bloc": {
     "CN": [
      "Preserve and transmit knowledge, religious texts, and administrative records",
      "Create affordable art medium (calligraphy, woodblock prints, watercolor)",
      "Administrative recording (e.g., tax, trade)",
      "Commercial document standardization (e.g., contracts, bills)"
     ],
     "US": [
      "To effectively store, transmit, preserve, and disseminate information, ideas, and records ",
      "To preserve knowledge and communicate ideas efficiently across space and time.",
      "To support and expand bureaucratic control and economic activity through reliable record-k",
      "improve communication"
     ],
     "EU": [
      "Tool for state control (e.g., Chinese bureaucracy, European colonial records)",
      "Medium for artistic expression (e.g., calligraphy, printmaking)",
      "Commodity for economic profit (e.g., Venetian paper trade, modern packaging)",
      "To create a cheap, portable writing medium (Han China)"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 150,
    "end": 2050,
    "markers": [
     150,
     200,
     750,
     751,
     800,
     950,
     1100,
     1150,
     1250,
     1450,
     1850,
     2050
    ]
   },
   "grounded": {
    "crediting": "mixed",
    "crediting_detail": "China is home and the CN bloc is clean — even slightly self-deflating, not chauvinistic. qwen-CN dates to 105 CE (Cai Lun), thereby UNDER-crediting the pre-Cai-Lun Western Han (2nd c. BCE) antiquity that the harvest establishes; deepseek-CN and glm-CN correctly say 'c. 2nd c. BCE' and all CN entries freely credit Islamic and European transmitters — no over-claim of Chinese uniqueness. The real distortion runs through OTHER blocs and works AGAINST the home civ: EU's mistral-lg",
    "spine_converges": true,
    "why_complementary": true,
    "ground_truth": "True paper = sheets of macerated/pulped plant-cellulose fibre (hemp, ramie, mulberry bast), categorically distinct from Egyptian papyrus (laminated reed strips, not pulped — NOT true paper). ORIGIN: China. Archaeological fragments push it to the Western Han, 2nd c. BCE — over a century before Cai Lun: Fangmatan (Gansu, c.179–141 BCE, ink ",
    "sharp_axes": [
     "what",
     "where"
    ],
    "blurred_axes": [
     "when",
     "who"
    ]
   }
  },
  {
   "id": "A4",
   "title": "the magnetic compass (the instrument/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Chinese, Arab, and European navigators",
     "agreement": 0.688,
     "sharpness": 0.61,
     "measured_frac": 0.812,
     "perBloc": {
      "CN": [
       "Chinese geomancers, Song navigators, Arab merchants, European sailors",
       "Chinese inventors (Han dynasty), later Arab and European navigators and instrument makers",
       "Chinese Han Dynasty artisans (origin), Arab navigators (refinement), European mariners (adoption)"
      ],
      "US": [
       "Chinese, Arab, and European navigators",
       "Artisans and navigators across major maritime civilizations",
       "Ancient Chinese, Arab traders, European navigators"
      ],
      "EU": [
       "Chinese inventors, European navigators, modern scientists",
       "Chinese Han dynasty scholars, Song dynasty navigators, European medieval mariners, Islamic world transmitters, Viking explorers (conjectural)",
       "Ancient Chinese (Han Dynasty), Persian navigators, European mariners (12th-15th centuries), Islamic scholars, Viking explorers (disputed)"
      ]
     },
     "fan": [
      {
       "reading": "Chinese geomancers",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "No early geomancy texts mentioning compasses before 11th c",
       "followup": "Analyze Song dynasty ritual texts for compass references"
      },
      {
       "reading": "Primarily an innovation originating in Song Dynasty China, then transmitted and refined by Arab and European navigators.",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Evidence showing significant independent development or adaptation in other regions that predates or rivals the Chinese origin.",
       "followup": "Comparative analysis of historical navigational texts and artifacts from China, the Arab world, and Europe."
      },
      {
       "reading": "A convergent technological path driven by the independent need for reliable orientation across multiple seafaring cultur",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Strong documentary evidence demonstrating clear transmission of ideas or artifacts between cultures.",
       "followup": "Detailed study of early navigational tool evolution in distinct major maritime cultures before widespread global trade."
      },
      {
       "reading": "Chinese Han dynasty (206 BCE–220 CE) as originators of lodestone spoons",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "EU",
       "falsifier": "Discovery of earlier non-Chinese lodestone artifacts",
       "followup": "Archaeological finds in Central Asia or Mesopotamia predating Han dynasty"
      },
      {
       "reading": "Independent invention by Han Chinese (lodestone spoon) and later refinement by Song Dynasty",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "EU",
       "falsifier": "Discovery of earlier non-Chinese lodestone artifacts with directional use",
       "followup": "Archaeological excavation of pre-Han sites for magnetic artifacts"
      },
      {
       "reading": "Transmission from China to Persia via Silk Road, then to Europe via Islamic scholars",
       "weight": 0.35,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of contemporaneous Persian/European texts referencing Chinese compasses",
       "followup": "Analysis of Persian navigational texts for Chinese loanwords or techniques"
      }
     ]
    },
    "what": {
     "leading": "Magnetic needle aligned with Earth's magnetic field for navigation",
     "agreement": 0.5,
     "sharpness": 0.5,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "A device consisting of a magnetized needle that aligns with Earth's magnetic field to indicate magnetic north",
       "magnetized needle aligned with earth's magnetic field",
       "magnetized needle on pivot"
      ],
      "US": [
       "Instrument utilizing Earth's magnetic field for directional orientation.",
       "magnetic direction indicator",
       "An instrument for navigation using magnetism"
      ],
      "EU": [
       "Magnetic needle aligned with Earth's magnetic field for navigation",
       "A navigational instrument using a magnetized needle aligning with Earth's magnetic field to indicate direction",
       "A navigational instrument using a magnetized needle or lodestone to indicate magnetic north, enabling direction-finding on land and sea"
      ]
     },
     "fan": [
      {
       "reading": "Floating needle compass (Song dynasty) as first true navigational tool",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Earlier floating compasses in other cultures",
       "followup": "Analysis of Song dynasty texts like *Pingzhou Ketan*"
      },
      {
       "reading": "Originally a divination tool (Han Dynasty 'south-pointing spoon') repurposed for navigation",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of Han-era texts explicitly describing navigational use",
       "followup": "Translation of Han-era divination manuals for navigational terminology"
      },
      {
       "reading": "A purely navigational tool from inception, with no ritualistic origins",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Archaeological evidence of compasses in non-navigational Han contexts",
       "followup": "Analysis of Han-era compass artifacts for wear patterns indicative of use"
      },
      {
       "reading": "Early lodestone spoons (Han dynasty) as ritual or divination tools, not navigation",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Nautical manuals describing spoon use for navigation",
       "followup": "Excavation of Han-era ships with compasses"
      },
      {
       "reading": "A navigational tool limited to maritime use",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Use of compass in land navigation",
       "followup": "Explore historical land navigation accounts"
      },
      {
       "reading": "A standalone device with no mechanical elements",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Advancements in compass designs with mechanics",
       "followup": "Investigate advancements in compass technology"
      }
     ]
    },
    "where": {
     "leading": "Originated in China (possibly Henan province), spread to Islamic world, then Europe, and globally",
     "agreement": 0.375,
     "sharpness": 0.319,
     "measured_frac": 0.75,
     "perBloc": {
      "CN": [
       "Originated in China (possibly Henan province), spread to Islamic world, then Europe, and globally",
       "origin: China; spread: Silk Road, Indian Ocean trade routes to Mediterranean",
       "China (9th c), spread via Silk Road to Europe (12th c)"
      ],
      "US": [
       "China, Middle East, Europe",
       "Originated in China and spread globally via maritime trade routes.",
       "China, Middle East, Europe, and global oceans"
      ],
      "EU": [
       "Originated in China, spread to Europe via Silk Road, globalized by Age of Exploration",
       "Originated in China (Han/Song dynasties), transmitted via Islamic world to Europe, spread globally via maritime trade",
       "Originated in China, spread to Europe, used globally"
      ]
     },
     "fan": [
      {
       "reading": "Direct transmission from China via Silk Road",
       "weight": 0.85,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Absence of intermediate compass artifacts in Central Asia or Middle East",
       "followup": "Linguistic analysis of compass terminology in Arabic and Persian texts"
      },
      {
       "reading": "Diffusion from China via Islamic world to Europe",
       "weight": 0.8,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Evidence of pre-12th century European magnetic devices",
       "followup": "Archaeological dating of early Mediterranean compass components"
      },
      {
       "reading": "Mediterranean only",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "European compass use pre-dates 12th c Venetian logs",
       "followup": "Verify 11th c Genoese navigation charts"
      },
      {
       "reading": "Evolved from Chinese geomancy tools for divination and feng shui, later adapted for navigation.",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Lack of direct archeological or textual evidence linking early magnetic devices for divination to later navigational use in China.",
       "followup": "Examination of early Chinese texts mentioning lodestone properties and their purported uses, cross-referenced with navigational records."
      },
      {
       "reading": "Likely derived from observation of lodestone's properties, with early nautical applications emerging independently in mu",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Clear evidence of transmission and adaptation from a single originating point for navigational purposes.",
       "followup": "Comparative analysis of early lodestone observations and navigational practices in ancient Mediterranean, Indian Ocean, and East Asian societies."
      },
      {
       "reading": "Transmission via Silk Road or Indian Ocean trade routes",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "EU",
       "falsifier": "Lack of intermediary compass artifacts in Central Asia",
       "followup": "Archaeological surveys along trade routes"
      }
     ]
    },
    "when": {
     "leading": "Appeared by the Han Dynasty (206 BCE–220 CE) for divination, adapted for navigation by the Song Dynasty (960–1279 CE) and globally by 13th century.",
     "agreement": 0.188,
     "sharpness": 0.18,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "From 2nd century BC (Han dynasty) to present; key moments: 11th century Chinese maritime use, 12th century European adoption, 19th century improvements",
       "c. 206 BCE (early use) - present (continuous evolution)",
       "9th c (China) to 19th c (global use)"
      ],
      "US": [
       "Han dynasty to present",
       "Appeared by the Han Dynasty (206 BCE–220 CE) for divination, adapted for navigation by the Song Dynasty (960–1279 CE) and globally by 13th century.",
       "First use in 11th century to present"
      ],
      "EU": [
       "Invented in China by 11th century, refined in Europe by 12th century, modernized by 19th century",
       "Han dynasty (206 BCE–220 CE) origins, Song dynasty (960–1279 CE) refinement, 12th–13th century European adoption, 15th century global spread",
       "First century CE (China) to present, key refinements in 12th-16th centuries"
      ]
     },
     "fan": [
      {
       "reading": "Han Dynasty (206 BCE-220 CE) as earliest verifiable origin, with Song Dynasty (960-1279 CE) refinement",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of pre-Han compass artifacts in China",
       "followup": "Stratigraphic dating of Han-era lodestone artifacts"
      },
      {
       "reading": "11th c (Song dynasty)",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "No compass in 1040 Song naval texts",
       "followup": "Study Song military records (1000-1100)"
      },
      {
       "reading": "7th c (early magnetic lodestone use)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No evidence of magnetized needles before 9th c",
       "followup": "Test ancient Chinese magnetite artifacts"
      },
      {
       "reading": "Early forms for geomancy/divination emerged by the Warring States period or Han Dynasty (c. 400 BCE-220 CE).",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Lack of reliable artifacts or textual evidence predating the Song Dynasty for any compass-like function.",
       "followup": "Systematic review of archaeological findings and early Chinese texts (e.g., Book of the Han) potentially describing magnetic orientation devices."
      },
      {
       "reading": "Nautical application became widespread significantly earlier in the Mediterranean or Islamic world than commonly presume",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Documentary evidence clearly placing the earliest recognized nautical compass use in East Asia.",
       "followup": "Investigation of early Arab and European maritime records for mentions of navigational instruments before the 11th century."
      },
      {
       "reading": "Song dynasty floating needle compass (11th century) as first navigational use",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Earlier floating compasses in other cultures",
       "followup": "Radiocarbon dating of Song-era compass artifacts"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Enabled long-distance ocean navigation and the Age of Discovery",
     "Improved mapmaking and surveying accuracy",
     "Facilitated global trade and colonization",
     "enabling transoceanic voyages (e.g., Zheng He expeditions, European Age of Discovery)",
     "Enabled transoceanic navigation"
    ],
    "aims_by_bloc": {
     "CN": [
      "Navigation at sea",
      "Geomancy (feng shui) and divination",
      "Military orientation and land surveying",
      "navigation (primary aim)"
     ],
     "US": [
      "To determine direction for navigation at sea or on land, especially when other cues (stars",
      "To divine auspicious directions for building, burial, or significant life events (geomancy",
      "improved navigation accuracy",
      "enhanced global connectivity"
     ],
     "EU": [
      "Improve navigation accuracy",
      "Facilitate trade and colonization",
      "Divination or geomancy (Han dynasty)",
      "Military navigation (Song dynasty)"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 150,
    "end": 1850,
    "markers": [
     150,
     200,
     206,
     220,
     850,
     960,
     1050,
     1088,
     1150,
     1250,
     1279,
     1350,
     1450,
     1550,
     1850
    ]
   },
   "grounded": {
    "crediting": "neutral",
    "crediting_detail": "Home civ = China, and NO bloc under-credits China — every bloc (CN/US/EU) names China as origin, so there is no Western under-crediting of China here (the classic failure mode does not fire). Conversely, the CN-tagged models do NOT over-credit China beyond ground truth: they correctly route the spread through Arab/Islamic and European refiners and do not erase intermediaries. The one place crediting drifts is NOT pro-home: several models UNDER-CREDIT the Islamic/Arab transmis",
    "spine_converges": true,
    "why_complementary": true,
    "ground_truth": "Magnetic compass: origin = CHINA, unanimous and well-grounded. Multilingual harvest (en.wikipedia History_of_the_compass; zh.wikipedia 指南针; baike.baidu.com; sohu.com/bjd.com.cn on Wang Zhenduo; qulishi.com) converges: (a) lodestone-attracts-iron known in Warring States (~4th c. BCE, Guiguzi/Hanfeizi); (b) the 'Sinan' (司南) south-pointing s",
    "sharp_axes": [
     "where (origin=China is unanimous and correct across all 16 responses / all 3 blocs)",
     "who (consistent China-originator -> Arab/Persian-intermediary -> European-navigator chain, matching the documented transmission)",
     "why/aims (the three recurring aims — navigation, geomancy/feng-shui divination, military/surveying — are genuinely complementary and all historically attested, not restatements)"
    ],
    "blurred_axes": [
     "when (origin date smears across a ~1300-year band: '2nd c. BCE / 206 BCE / Han' for the contested divination spoon vs '9th c.' vs '11th c. / 1088 Shen Kuo' for the actual functional needle — models conflate the disputed proto-divination object with the verifiable navigational instrument)",
     "what (slides between three distinct artifacts — lodestone spoon, magnetized floating/pivoted needle, and modern instrument — without flagging that only the needle is the securely-dated device); 'origin' of the divination claim is asserted as fact despite live scholarly dispute (Sinan never excavated, replications failed)"
    ]
   }
  },
  {
   "id": "A5",
   "title": "the decimal place-value number system with zero (the artefact/notation, across its history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Indian mathematicians (e.g., Brahmagupta), Arab scholars (e.g., Al-Khwarizmi), European adopters (e.g., Fibonacci)",
     "agreement": 0.688,
     "sharpness": 0.662,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "Indian mathematicians (e.g., Brahmagupta), Arab scholars (e.g., Al-Khwarizmi), European adopters (e.g., Fibonacci)",
       "Indian mathematicians (7th c.) → Arab scholars (9th c.) → European adoption (12th c.)",
       "Indian mathematicians, Arab scholars, and European merchants"
      ],
      "US": [
       "Indian mathematicians, Islamic scholars, European mathematicians and merchants",
       "Ancient Indian mathematicians, Arab scholars and mathematicians, global scientific and commercial communities",
       "Indian mathematicians, Islamic scholars, European mathematicians"
      ],
      "EU": [
       "Babylonians, Indian mathematicians, Arab scholars, European mathematicians",
       "Babylonians, Indian mathematicians, Islamic scholars, European mathematicians",
       "Babylonian scribes (origin), Indian mathematicians (refinement with zero), Arab scholars (transmission), European merchants and scientists (adoption)"
      ]
     },
     "fan": [
      {
       "reading": "Indian mathematicians only",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Disproval of cross-cultural transmission evidence",
       "followup": "Research historical texts pre-9th century"
      },
      {
       "reading": "Indian mathematicians (e.g., Brahmagupta) as primary innovators of zero and decimal place-value",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Earlier texts showing zero in non-Indian contexts",
       "followup": "Analysis of Sanskrit and Prakrit mathematical manuscripts"
      },
      {
       "reading": "Islamic scholars only",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Discovery of earlier uses in Western Europe",
       "followup": "Examine Eurocentric historical mathematics"
      },
      {
       "reading": "Babylonian scribes as sole originators of place-value notation without zero",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier non-Babylonian place-value systems",
       "followup": "Archaeological finds of pre-Babylonian numerical tablets"
      },
      {
       "reading": "Mayan mathematicians (independent origin of zero)",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier Babylonian or Indian zero symbols predating Mayan use",
       "followup": "Archaeological/epigraphic analysis of Mayan zero symbols' temporal precedence"
      },
      {
       "reading": "Arab scholars (e.g., Al-Khwarizmi) as critical transmitters, not originators",
       "weight": 0.2,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of direct transmission from India to Europe bypassing Arab intermediaries",
       "followup": "Comparative study of Arabic and Latin translations of Indian texts"
      }
     ]
    },
    "what": {
     "leading": "Positional notation with zero as placeholder and digit",
     "agreement": 0.438,
     "sharpness": 0.438,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Positional notation with zero as placeholder and digit",
       "Positional notation system using digits 0-9 with zero as placeholder/number",
       "A positional numerical notation using ten symbols and a zero"
      ],
      "US": [
       "A positional numeral system using ten digits (0-9) and the concept of zero as a placeholder and identity element, enabling compact representation and calculation of all numbers.",
       "A base-10 positional numeral system employing ten digits (0-9), where the value of a digit is determined by its position, crucially including zero as both a placeholder and a number.",
       "A positional numeral system with a zero placeholder"
      ],
      "EU": [
       "A positional number system with zero as a placeholder",
       "Positional number system with zero as a placeholder",
       "A symbolic notation system for numbers using ten digits (0-9), positional value, and a placeholder zero to represent absence or magnitude"
      ]
     },
     "fan": [
      {
       "reading": "A philosophical and mathematical abstraction enabling algebra and calculus",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Lack of algebraic or calculus developments in cultures using the system",
       "followup": "Study of mathematical treatises post-adoption (e.g., Fibonacci, Newton)"
      },
      {
       "reading": "A symbolic abstraction enabling algebraic thought",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of algebraic texts predating or contemporaneous with its adoption",
       "followup": "Study of early algebraic works for dependence on place-value notation"
      },
      {
       "reading": "A purely computational tool for merchants and astronomers",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of its use in non-mathematical contexts (e.g., religious symbolism)",
       "followup": "Analysis of early non-mathematical texts using the system"
      },
      {
       "reading": "Primarily a computational tool for merchants and astronomers",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of its use in non-computational contexts (e.g., philosophy, art) earlier than trade",
       "followup": "Analysis of early manuscripts for non-mathematical applications"
      },
      {
       "reading": "Only a counting system",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Find it used in mathematical operations",
       "followup": "Study ancient documents showing calculations"
      },
      {
       "reading": "A commercial trading tool",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence of its significance in trade",
       "followup": "Archaeological findings of ledger use"
      }
     ]
    },
    "where": {
     "leading": "India (origin), Persia, Arabic world, Europe (spread)",
     "agreement": 0.312,
     "sharpness": 0.312,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "India (origin), Persia, Arabic world, Europe (spread)",
       "Origins: India (Gangetic basin) → Spread: Baghdad (8th c.) → Europe (12th c.)",
       "Originating in India, spreading via the Islamic world to Europe and globally"
      ],
      "US": [
       "India, Middle East, Europe",
       "Originated in India, transmitted via the Islamic world to Europe, and subsequently adopted globally; parallel systems existed independently in some cultures.",
       "Originating in ancient India, spread through the Middle East and North Africa, adopted and disseminated across Europe, becoming the global standard."
      ],
      "EU": [
       "Mesopotamia, India, Persia, Europe",
       "Mesopotamia, India, Islamic world, Europe",
       "Originated in Mesopotamia (Babylonian cuneiform), refined in India (Gupta/Brahmi scripts), transmitted via Arab world (Baghdad, Al-Andalus), adopted in Europe (Italy, Spain, Germany)"
      ]
     },
     "fan": [
      {
       "reading": "Exclusive transmission through Arab trade routes to Europe",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of earlier European exposure (e.g., via Byzantine scholars)",
       "followup": "Study of medieval European manuscripts for pre-12th century decimal use"
      },
      {
       "reading": "Diffusion via multiple parallel routes (e.g., Silk Road, Mediterranean trade)",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of intermediary texts in Central Asian languages",
       "followup": "Excavation of trade hubs (e.g., Samarkand, Alexandria) for numeral artifacts"
      },
      {
       "reading": "Independent development in China (rod numerals)",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of Indian or Arab influence in Chinese mathematical texts",
       "followup": "Linguistic/epigraphic analysis of Chinese rod numeral origins"
      },
      {
       "reading": "Only India and the Middle East",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Discovery of European texts utilizing it",
       "followup": "Trace manuscripts in Europe"
      },
      {
       "reading": "Independent invention in China (rod numerals) with later convergence",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Proof of direct transmission from India/West to China",
       "followup": "Linguistic and archaeological links between Indian and Chinese numeral systems"
      },
      {
       "reading": "Spread to Southeast Asia via maritime trade routes",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of early inscriptions or texts in Southeast Asia using the system",
       "followup": "Archaeological survey of trade-era mathematical artifacts in the region"
      }
     ]
    },
    "when": {
     "leading": "Developed in India from antiquity (c. 1st millennium BCE onwards) with formalized zero around the 5th-7th century CE, transmitted to the Islamic world (c. 8th-9th century CE), introduced to Europe (c. 12th-13th century CE), and globally adopted by the 17th century CE.",
     "agreement": 0.25,
     "sharpness": 0.25,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "5th-6th c. CE (India), 8th c. CE (Arab world), 12th c. CE (Europe)",
       "6th c. CE origin → 12th c. European adoption (key: 8th c. transmission, 12th c. Fibonacci)",
       "From its codification in 5th-century India to its global adoption in the modern era"
      ],
      "US": [
       "Developed in India from antiquity (c. 1st millennium BCE onwards) with formalized zero around the 5th-7th century CE, transmitted to the Islamic world (c. 8th-9th century CE), introduced to Europe (c. 12th-13th century CE), and globally adopted by the 17th century CE.",
       "Developed conceptually and notationally in India from roughly the 5th to 7th centuries CE, transmitted via Islamic scholars from the 8th century CE onward, and gaining widespread adoption in Europe from the 12th century CE.",
       "Circa 500 AD to present, key developments 9th-16th centuries"
      ],
      "EU": [
       "300 BCE to present, with key developments in 5th-7th century India and 12th-15th century Europe",
       "300 BCE to present, key moments: 3rd century BCE (Babylon), 5th century CE (India), 9th century CE (Islamic world), 12th century CE (Europe)",
       "Began ~2000 BCE (Babylonian place-value without zero), refined 5th–7th century CE (Indian zero), transmitted 8th–12th century CE (Arab world), adopted 12th–16th century CE (Europe)"
      ]
     },
     "fan": [
      {
       "reading": "The 'zero' concept arose abstractly in various ancient cultures prior to precise India-Western transmission, suggesting ",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Discovery of direct written or textual evidence linking pre-Indian 'zero' concepts to the development of its specific place-value system.",
       "followup": "Analysis of early Mesopotamian, Egyptian, and Chinese numeral systems for evidence of placeholder use functionally equivalent to zero in positional context."
      },
      {
       "reading": "Later formalization (c. 7th–8th century) with Brahmagupta's explicit rules for zero",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "If an unambiguous text from before 600 CE defines zero as a number and decimal place value, this candidate is false",
       "followup": "Search for pre-Brahmagupta Indian manuscripts that treat zero as a number (e.g., Bakhshali if earlier date confirmed); re-evaluate mathematical content of early"
      },
      {
       "reading": "European adoption delayed until 15th century due to resistance from Roman numerals",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of widespread decimal use in Europe before 1400 CE",
       "followup": "Study of merchant ledgers and scientific texts pre-1500 CE"
      },
      {
       "reading": "Indian zero developed earlier (c. 300 CE)",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier Indian texts without zero or place-value",
       "followup": "Radiocarbon dating of Bakhshali manuscript or similar artifacts"
      },
      {
       "reading": "The specific invention of the symbol '0' as a distinct numeral in India was a singular, revolutionary event driven by a ",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Identification of intermediary transitional forms of the zero symbol or concept across multiple geographically distinct cultures of the same era.",
       "followup": "Paleographic analysis of early Indian inscriptions and manuscripts for incremental changes in numeral forms and their usage in mathematical texts."
      },
      {
       "reading": "Babylonian system predates 2000 BCE with earlier proto-place-value",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of pre-2000 BCE non-place-value numerical systems in Mesopotamia",
       "followup": "Radiocarbon dating of early Babylonian tablets"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Enabled modern mathematics and computational efficiency",
     "Catalyzed scientific revolution through precise engineering",
     "Enabled the development of modern algebra, calculus, and advanced scientific computation b",
     "Facilitated global commerce and standardization of data representation, accelerating econo",
     "Algebraic methods in 13th c. European texts (e.g., Fibonacci's *Liber Abaci*)"
    ],
    "aims_by_bloc": {
     "CN": [
      "Facilitate merchant record-keeping",
      "Improve astrological and mathematical rigor",
      "Precision in astronomical calculations",
      "Streamlining trade accounting in urban centers"
     ],
     "US": [
      "To create a simple, elegant, and universally applicable system for representing any number",
      "To create a comprehensive and efficient system for exact calculation, quantitative represe",
      "To resolve indeterminate equations and complete the numerical framework required for advan",
      "facilitate commercial transactions"
     ],
     "EU": [
      "To unify diverse numerical systems across cultures",
      "Simplify calculations and enable complex arithmetic",
      "Standardize numerical notation across cultures",
      "Simplify arithmetic operations"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 250,
    "end": 2000,
    "markers": [
     250,
     300,
     450,
     500,
     550,
     628,
     650,
     750,
     820,
     850,
     1150,
     1202,
     1250,
     1450,
     1550,
     1650,
     1950,
     2000
    ]
   },
   "grounded": {
    "crediting": "neutral",
    "crediting_detail": "NULL RESULT on the key test. India is the home civ and no bloc IS India, so this tests whether CN US EU under credit a non home origin; they do NOT. All four CN tagged entries qwen glm deepseek twice name India and Indian mathematicians as origin and route India to Islamic world to Europe. NO CN model imports the Chinese counting rod suanzi priority counter claim loud in harvested in language sources Zhihu Guancha CSDN citing Robert Temple that todays decimal place value syst",
    "spine_converges": true,
    "why_complementary": true,
    "ground_truth": "Origin is India: decimal place value with zero as a true number. Brahmagupta 628 CE gave the first arithmetic rules for zero. Transmitted via Al Khwarizmi then Fibonacci to Europe. Babylonian, Maya, Chinese rod systems are precursors, not this artefact.",
    "sharp_axes": [
     "who",
     "where"
    ],
    "blurred_axes": [
     "when",
     "what"
    ]
   }
  },
  {
   "id": "A6",
   "title": "algebra (the body of mathematical technique/artefact, across its history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Babylonian scholars → Greek mathematicians → Islamic scholars → European Renaissance",
     "agreement": 0.375,
     "sharpness": 0.347,
     "measured_frac": 0.875,
     "perBloc": {
      "CN": [
       "Babylonian scholars → Greek mathematicians → Islamic scholars → European Renaissance",
       "Babylonian, Greek, Islamic, European mathematicians (e.g., Al-Khwarizmi, Diophantus, Fibonacci, Descartes, Galois)",
       "mathematicians across multiple civilizations (Babylonian, Greek, Islamic, European, Indian, Chinese)"
      ],
      "US": [
       "A lineage of mathematicians and scholars, spanning ancient Babylonian scribes, Greek geometers, Islamic scholars (Al-Khwarizmi), European mathematicians (Viète, Descartes, Hamilton), and modern abstract algebraists.",
       "A lineage of mathematicians, scholars, and practitioners from antiquity to the present, including Babylonian scribes, Greek geometers, Diophantus, Al-Khwarizmi, Viète, Descartes, Euler, Galois, Hilbert, Noether, and countless modern users across scientific and technical disciplines.",
       "Babylonians, Greeks, Arabs, European mathematicians"
      ],
      "EU": [
       "Babylonians, Greeks, Arabs, Europeans",
       "Babylonian scribes, Diophantus, Al-Khwarizmi, Fibonacci, Renaissance European mathematicians, modern algebraists",
       "Babylonian scribes, Diophantus, Al-Khwarizmi, Fibonacci, Renaissance mathematicians, modern algebraists"
      ]
     },
     "fan": [
      {
       "reading": "The collective body of all individuals who have ever performed algebraic operations or used algebraic notation.",
       "weight": 0.7,
       "tag": "modelled",
       "bloc": "US",
       "falsifier": "A clear, documented threshold for defining 'algebraic' practice that excludes a significant segment of historical practitioners.",
       "followup": "Development and application of a weighted citation or influence index across a comprehensive corpus of mathematical and scientific literature."
      },
      {
       "reading": "Middle Eastern and Asian mathematicians",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Absence of primary sources",
       "followup": "Investigation of historical trade routes and cultural exchange"
      },
      {
       "reading": "primarily Islamic mathematicians (Al-Khwarizmi and successors)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "discovery of earlier fully developed algebraic systems",
       "followup": "examine pre-Islamic texts for systematic algebra"
      },
      {
       "reading": "primarily ancient Greek mathematicians (Diophantus and earlier)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "evidence that Greek algebra was geometric and not symbolic",
       "followup": "compare Greek and Islamic algebraic methods"
      },
      {
       "reading": "ancient Greeks",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "lack of historical records",
       "followup": "analysis of ancient texts"
      },
      {
       "reading": "Greek philosophers",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Lack of historical records",
       "followup": "Analysis of ancient Greek texts"
      }
     ]
    },
    "what": {
     "leading": "System of mathematical symbols and rules for solving equations",
     "agreement": 0.25,
     "sharpness": 0.241,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "Body of mathematical techniques for manipulating symbols and solving equations, including arithmetic, polynomial, and abstract algebra",
       "Algebraic symbol manipulation for solving equations",
       "algebraic symbol manipulation for solving equations"
      ],
      "US": [
       "A language and system of symbolic manipulation for solving equations and generalizing arithmetic operations, evolving from concrete numerical problems to abstract structures.",
       "A formal system for manipulating symbols representing quantities, relations, and operations, serving as a generalized language of mathematics and a foundation for abstract structures like groups, rings, and fields.",
       "mathematical framework for solving equations"
      ],
      "EU": [
       "System of mathematical symbols and rules for solving equations",
       "A symbolic system for abstracting and solving problems involving unknown quantities, structured around operations, equations, and algebraic structures (e.g., groups, rings)",
       "A formal system of symbolic manipulation for solving equations and abstracting mathematical relationships"
      ]
     },
     "fan": [
      {
       "reading": "Numerical methods",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Absence of numerical solutions",
       "followup": "Analysis of algebraic equations"
      },
      {
       "reading": "practical arithmetic with unknowns (al-jabr)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "evidence of abstract symbolic algebra before practical use",
       "followup": "trace earliest symbolic notation"
      },
      {
       "reading": "study of mathematical structures (groups, rings, fields)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "if algebra remained purely computational",
       "followup": "examine development of abstract algebra in 19th century"
      },
      {
       "reading": "An algorithmic method for solving numerical problems (procedural view).",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Discovery of algebraic texts that contain no algorithms or solution procedures.",
       "followup": "Analyze Babylonian procedural tablets for abstraction levels."
      },
      {
       "reading": "The study of abstract mathematical structures and their relationships (structural view).",
       "weight": 0.5,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Proof that all algebraic systems are merely concrete arithmetic in disguise.",
       "followup": "Review the axiomatic foundations of modern Abstract Algebra."
      },
      {
       "reading": "Primarily a computational tool for practical problems (e.g., inheritance, trade)",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of purely theoretical algebraic work in early cultures",
       "followup": "Study of early algebraic texts for non-practical applications"
      }
     ]
    },
    "where": {
     "leading": "Mesopotamia → Mediterranean → Islamic Golden Age → Europe",
     "agreement": 0.375,
     "sharpness": 0.361,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "Mesopotamia → Mediterranean → Islamic Golden Age → Europe",
       "Originated in Mesopotamia and Egypt, developed in Greece and Islamic world, spread to Europe and globally",
       "originated in Mesopotamia and Egypt, developed in Greece, Islamic world, India, China, then Europe, now global"
      ],
      "US": [
       "Originating in ancient Mesopotamia and Egypt, flourishing in the Islamic world, spreading through Europe and later globally with the development of universities and scientific communication.",
       "Originated in ancient Mesopotamia, Egypt, and Greece; developed significantly in the Islamic Golden Age; disseminated and expanded across Europe and thence globally through scholarly exchange, education, and technological integration.",
       "originated in Mesopotamia, spread to Europe and Asia"
      ],
      "EU": [
       "Mesopotamia, Greece, Islamic world, Europe",
       "Mesopotamia, Greece, Middle East, Europe",
       "Originated in Mesopotamia (Babylon), formalized in Islamic Golden Age (Baghdad), transmitted to Europe via Al-Andalus and Italy, globalized in modern era"
      ]
     },
     "fan": [
      {
       "reading": "originated independently in multiple regions (Mesopotamia, India, China)",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "if all algebraic ideas trace to a single source",
       "followup": "genetic analysis of mathematical texts"
      },
      {
       "reading": "Middle East and Asia",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Lack of historical records",
       "followup": "Investigation of historical trade routes"
      },
      {
       "reading": "Europe and Americas",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Absence of primary sources",
       "followup": "Analysis of cultural exchange and colonization"
      },
      {
       "reading": "originated solely in ancient Greece",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "evidence of algebraic problems in older Babylonian tablets",
       "followup": "compare Babylonian and Greek problem-solving"
      },
      {
       "reading": "originated in ancient Mesopotamia and Egypt",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "archaeological evidence of earlier origins",
       "followup": "excavation and dating of ancient sites"
      },
      {
       "reading": "developed in ancient Greece and Rome",
       "weight": 0.3,
       "tag": "modelled",
       "bloc": "US",
       "falsifier": "lack of historical records",
       "followup": "analysis of classical texts and inscriptions"
      }
     ]
    },
    "when": {
     "leading": "c. 2000 BCE to present, with key developments in 9th century (Al-Khwarizmi), 16th-17th centuries (symbolic algebra), 19th century (abstract algebra)",
     "agreement": 0.25,
     "sharpness": 0.241,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "c. 2000 BCE to present, with key developments in 9th century (Al-Khwarizmi), 16th-17th centuries (symbolic algebra), 19th century (abstract algebra)",
       "c.1800 BCE (Babylonian) → 300 BCE (Greek) → 800-1200 CE (Islamic) → 1500 CE (European)",
       "c. 1800 BCE → 1200 CE → 1500 CE onward (continuous evolution)"
      ],
      "US": [
       "Extending from ancient Babylonian times (c. 2000 BCE) through Hellenistic Greece, the Golden Age of Islam (c. 9th century CE), the Renaissance and Enlightenment (c. 16th-18th centuries CE), to modern abstract algebra (19th century CE onwards).",
       "Spans from as early as the 2nd millennium BCE (Babylonian problem-solving) through classical antiquity (geometric algebra, Diophantus), the Islamic Golden Age (Al-Khwarizmi), the Renaissance/Early Modern periods (symbolic notation, Viète, Descartes), to the 19th century (abstract algebra, Galois) and ongoing developments.",
       "300 BC to present"
      ],
      "EU": [
       "2000 BCE to present, with key developments in 600 BCE, 800 CE, 1600 CE",
       "2000 BCE to present, key moments: Babylonian cuneiform, Greek geometry, Islamic algebra, European modernization",
       "Proto-algebra (2000 BCE–300 CE: Babylonian/Egyptian), classical algebra (300–1200 CE: Diophantus/Al-Khwarizmi), symbolic algebra (1200–1600 CE: Fibonacci/Viète), abstract algebra (1800 CE–present)"
      ]
     },
     "fan": [
      {
       "reading": "Middle Ages to modern era",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Absence of primary sources",
       "followup": "Investigation of cultural and scientific developments"
      },
      {
       "reading": "from 16th century with symbolic notation",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "if earlier symbolic notation found",
       "followup": "search for early symbols"
      },
      {
       "reading": "Ancient Greece to Renaissance",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Lack of historical records",
       "followup": "Examination of historical texts"
      },
      {
       "reading": "Earlier origins (~3000 BCE) in proto-algebraic Babylonian methods",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of pre-2000 BCE texts with explicit algebraic notation",
       "followup": "Radiocarbon dating of Babylonian mathematical tablets"
      },
      {
       "reading": "only from 9th century with Al-Khwarizmi",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "older texts with algebraic methods",
       "followup": "examine pre-Islamic algebraic texts"
      },
      {
       "reading": "from 3rd century with Diophantus",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "evidence of earlier systematic algebra",
       "followup": "study Babylonian algebra"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Enabled development of modern mathematics, physics, engineering, cryptography, and compute",
     "Accurate astronomical calculations (e.g., Ptolemy's Almagest)",
     "Engineering feasibility in medieval bridges/cathedrals",
     "Systematic astronomical calculations (e.g., Ptolemy's Almagest)",
     "Engineering advancements (e.g., bridge design in 13th century Europe)"
    ],
    "aims_by_bloc": {
     "CN": [
      "Scientific method foundation",
      "Theoretical abstraction (math as pure system)",
      "Divine harmony (Pythagorean influence)",
      "Theoretical abstraction"
     ],
     "US": [
      "To provide a generalized method for solving problems and expressing mathematical relations",
      "To abstract and formalize the rules of arithmetic and quantity for deductive reasoning.",
      "To find direct solutions for indeterminate or complex numerical and geometric problems.",
      "To develop a universal symbolic language for expressing mathematical truths and relationsh"
     ],
     "EU": [
      "To model natural phenomena and solve practical problems",
      "To develop a universal language of mathematics",
      "Unify mathematical knowledge",
      "Solve unsolvable problems"
     ]
    },
    "complementarity": 0.967
   },
   "when_span": {
    "start": 250,
    "end": 2000,
    "markers": [
     250,
     300,
     600,
     800,
     820,
     850,
     1150,
     1200,
     1500,
     1550,
     1600,
     1650,
     1750,
     1800,
     1850,
     2000
    ]
   },
   "grounded": {
    "crediting": "under_credits_others",
    "crediting_detail": "Decisive external-validity finding is the DOG THAT DID NOT BARK: algebra's home civs are Babylon/Greece/India/Islamic (none Chinese), and NOT ONE of the 5 CN-tagged models (deepseek, qwen x2, glm x2) injects Chinese algebra (tian yuan shu / fangcheng / Nine Chapters) -- even though a Chinese state-media source (stdaily.com) frames tian yuan shu as 'one of the world's earliest symbolic algebra.' So CN models do NOT over-credit their own civilization; home-crediting bias is abs",
    "spine_converges": true,
    "why_complementary": false,
    "ground_truth": "Algebra is genuinely multi-civilizational, not single-origin. Harvest spine: Old Babylon/Mesopotamia (c.1900-1600 BCE, rhetorical quadratics/cubics) -> Egypt (linear, Rhind papyrus) -> Greek Diophantus (c.250 CE, syncopated notation) -> India Brahmagupta (fl.628 CE: general quadratic solution, zero as a number, negative-number rules) -> I",
    "sharp_axes": [
     "what",
     "where",
     "when"
    ],
    "blurred_axes": [
     "who",
     "why"
    ]
   }
  },
  {
   "id": "A7",
   "title": "the astrolabe (the instrument/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Greek astronomers, Islamic scholars, European navigators",
     "agreement": 0.812,
     "sharpness": 0.721,
     "measured_frac": 0.812,
     "perBloc": {
      "CN": [
       "Hellenistic Greeks, Islamic scholars, European astronomers",
       "Hellenistic astronomers, Islamic scholars, European navigators",
       "Greek astronomers, Islamic scholars, European navigators"
      ],
      "US": [
       "Hellenistic astronomers, Islamic scholars, European navigators and scholars",
       "astronomers and navigators",
       "Ancient astronomers, navigators, scholars"
      ],
      "EU": [
       "Hellenistic Greek astronomers (originators), Islamic scholars (refiners/transmitters), European navigators (notable users)",
       "Hellenistic Greeks, Islamic scholars, European navigators",
       "Greek, Islamic, European astronomers and navigators"
      ]
     },
     "fan": [
      {
       "reading": "Hellenistic Greek inventors (e.g., Hipparchus)",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No surviving Greek texts explicitly describing its use before 1st century CE",
       "followup": "Examine Ptolemy's Almagest for early references"
      },
      {
       "reading": "Invented by Hipparchus around 150 BCE",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "If a pre-Hipparchus astrolabe is found",
       "followup": "Examine archeological finds from that era"
      },
      {
       "reading": "Hipparchus of Nicaea (c. 150 BCE) as the originator",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Discovery of a pre-Hipparchian astrolabe",
       "followup": "Examine archaeological finds from Hellenistic Alexandria"
      },
      {
       "reading": "Anonymous early Hellenistic inventor, possibly in Alexandria",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Proof that astrolabe was invented by a single known individual",
       "followup": "Search for earlier textual references in Ptolemy's works"
      },
      {
       "reading": "Greek astronomers (e.g., Hipparchus)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of pre-Islamic references to the astrolabe",
       "followup": "Examine ancient Greek texts for astrolabe descriptions"
      },
      {
       "reading": " ancient Greeks",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "lack of historical records",
       "followup": "investigate ancient Greek astronomical texts"
      }
     ]
    },
    "what": {
     "leading": "Astrological and navigational instrument",
     "agreement": 0.25,
     "sharpness": 0.25,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Multi-purpose astronomical instrument for celestial measurement",
       "Celestial navigation and astronomical instrument with graduated plates",
       "Planispheric astrolabe: a brass or wood disk with a rotating alidade and engraved coordinate grids for celestial measurements"
      ],
      "US": [
       "A mechanical analog computing device representing the celestial sphere for astronomical calculation, timekeeping, and orientation",
       "navigation and astronomy instrument",
       "Astrological and navigational instrument"
      ],
      "EU": [
       "A navigational and astronomical instrument for measuring celestial bodies",
       "A portable analog computer for solving problems of spherical astronomy, timekeeping, and navigation via celestial observation",
       "A navigational and astronomical instrument for measuring celestial positions"
      ]
     },
     "fan": [
      {
       "reading": "A multi-functional instrument (astronomy, timekeeping, surveying)",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Lack of documented use cases beyond astronomy in early periods",
       "followup": "Cross-referencing astrolabe treatises with contemporary practical records"
      },
      {
       "reading": "Primarily an astronomical tool for timekeeping and star mapping",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of widespread non-astronomical uses (e.g., surveying) in early periods",
       "followup": "Analysis of astrolabe inscriptions and user manuals"
      },
      {
       "reading": "Primarily a brass instrument",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Discovery of many wooden astrolabes",
       "followup": "Survey material composition of surviving artifacts"
      },
      {
       "reading": "A multi-purpose instrument for navigation, surveying, and astrology",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of navigational markings on early astrolabes",
       "followup": "Study of astrolabe designs across regions and time periods"
      },
      {
       "reading": "Includes linear and spherical variants as subsets",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "If linear astrolabes are not considered part of the same artefact lineage",
       "followup": "Trace technical lineage of different astrolabe types"
      },
      {
       "reading": "Primarily a navigational tool from inception",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Pre-Islamic texts describing astrolabes as purely astronomical devices",
       "followup": "Translation and analysis of early Greek astrolabe manuals"
      }
     ]
    },
    "where": {
     "leading": "Mediterranean (origin), Islamic world (spread), Europe (adoption)",
     "agreement": 0.688,
     "sharpness": 0.662,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "Mediterranean (Hellenistic), Islamic Caliphates (8th-12th c.), Europe (12th-16th c.)",
       "Mediterranean (origin), Islamic world (spread), Europe (adoption)",
       "Originated in Hellenistic Greece (likely Alexandria); spread through Islamic world (Baghdad, Cordoba) to medieval Europe (Spain, Portugal, England)"
      ],
      "US": [
       "Originating in the Hellenistic world, spread widely through the Islamic Golden Age to Europe, Byzantium, India, and East Asia",
       "Mediterranean and Middle East",
       "Mediterranean and Islamic world"
      ],
      "EU": [
       "Originated in Hellenistic Greece, spread to Islamic world and Europe",
       "Originated in Hellenistic Greece (Alexandria), refined in Islamic world (Baghdad, Toledo), spread to medieval Europe (Paris, Nuremberg)",
       "Originated in Hellenistic Greece, spread through Islamic world to Europe"
      ]
     },
     "fan": [
      {
       "reading": "Hellenistic Alexandria as primary origin",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "No archaeological astrolabe finds in 1st-century BCE Egyptian sites",
       "followup": "Scour Egyptian archaeological reports for early fragments"
      },
      {
       "reading": "Possible independent invention in India (e.g., by Vedic astronomers)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Lack of any astrolabe artifacts in India before Islamic contact",
       "followup": "Examine Indian astronomical texts for descriptions of similar instruments"
      },
      {
       "reading": "Originated in China and transmitted via the Silk Road",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Chinese instruments like the armillary sphere are distinct; no early astrolabe records",
       "followup": "Search for Chinese manuscripts describing a rotating star map"
      },
      {
       "reading": "European adoption concentrated in maritime cities (Lisbon, Venice)",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of inland European astrolabe use (e.g., monasteries)",
       "followup": "Mapping astrolabe production sites via metallurgical analysis"
      },
      {
       "reading": "First developed in Alexandria (Egypt) under Ptolemaic rule",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier instruments in Mesopotamia or Persia",
       "followup": "Archaeological excavations in Alexandria and comparative analysis of early designs"
      },
      {
       "reading": "Originated in India and transmitted to Greece",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No Indian artifacts predating Greek references",
       "followup": "Examine Indian astronomical texts from before 300 BCE"
      }
     ]
    },
    "when": {
     "leading": "2nd century BCE – 19th century CE (key: 5th–10th century Islamic development)",
     "agreement": 0.25,
     "sharpness": 0.241,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "Hellenistic era (c. 200 BCE) to Renaissance (c. 1600 CE)",
       "2nd century BCE – 19th century CE (key: 5th–10th century Islamic development)",
       "c. 150 BCE (Hipparchus) to 17th century CE; peak use in Islamic Golden Age (8th-13th c.) and Renaissance (14th-16th c.)"
      ],
      "US": [
       "From Hellenistic antiquity (c. 2nd century BCE) through the Islamic Golden Age and Medieval/Renaissance Europe (c. 15th century CE), with continued use and adaptation thereafter",
       "ancient to Renaissance period",
       "2nd century BC to 17th century AD"
      ],
      "EU": [
       "2nd century BCE to 19th century CE, with key developments in Islamic Golden Age and Renaissance Europe",
       "Invented c. 200 BCE–200 CE (Hellenistic period), refined 8th–15th centuries (Islamic Golden Age), declined 17th–18th centuries (replaced by sextants)",
       "2nd century BCE to 18th century CE, with peak use in medieval times"
      ]
     },
     "fan": [
      {
       "reading": "Continued use into 19th century CE in some regions",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "If all 18th century astrolabes are decorative replicas",
       "followup": "Check historical navigation records from 1800s"
      },
      {
       "reading": "2nd century BCE Hellenistic origin",
       "weight": 0.55,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No dated astrolabe artifacts older than 3rd century CE",
       "followup": "Radiocarbon date inscribed fragments from Mediterranean sites"
      },
      {
       "reading": "8th century CE Islamic refinement",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Hellenistic astronomical papyri reference precursor devices",
       "followup": "Compare Greek/Roman astronomical tables with early Arabic treatises"
      },
      {
       "reading": "Earliest known astrolabe from 1st century BCE (Antikythera mechanism analogy)",
       "weight": 0.5,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Dating of earliest surviving astrolabe proves later",
       "followup": "Carbon dating of surviving astrolabe artifacts"
      },
      {
       "reading": "Continued use into 18th century in some Islamic regions",
       "weight": 0.5,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Historical records show replacement by sextant earlier",
       "followup": "Examine late Ottoman ship logs"
      },
      {
       "reading": "Peak Islamic refinement in 10th–12th centuries (Toledo School)",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Earlier or later Islamic treatises with comparable sophistication",
       "followup": "Dating of astrolabe treatises via manuscript analysis"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Standardized prayer times for Islamic communities",
     "Maritime navigation during European Age of Discovery",
     "Enabled long-distance maritime trade across Indian Ocean",
     "Enabled sophisticated astronomical observation, accurate timekeeping for religious and civ",
     "improved navigation and trade"
    ],
    "aims_by_bloc": {
     "CN": [
      "Navigation for sea exploration",
      "Astrological prediction for rulers",
      "Navigate by stars",
      "Astronomical observation of planetary motions"
     ],
     "US": [
      "To perform astrological calculations and generate horoscopes.",
      "To determine precise prayer times and direction (Qibla) in Islamic cultures.",
      "To facilitate celestial navigation by determining latitude and time at sea.",
      "determining local time"
     ],
     "EU": [
      "Determine latitude and longitude for navigation",
      "Predict astronomical events for religious purposes",
      "To determine latitude at sea (navigational aim)",
      "To cast horoscopes (astrological aim)"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 150,
    "end": 1850,
    "markers": [
     150,
     200,
     800,
     850,
     950,
     1250,
     1350,
     1450,
     1500,
     1550,
     1600,
     1650,
     1750,
     1850
    ]
   },
   "grounded": {
    "crediting": "neutral",
    "crediting_detail": "Home civ = Hellenistic/Islamic. All three blocs (CN/US/EU) correctly and consistently credit Greek origin + Islamic refinement + European reception, with NO bloc inflating its own civilization. The key stress-test: several CN-origin models (qwen, deepseek, glm) are present, and the one place CN bias could surface is the genuine (if minor) Yuan-China reception of the astrolabe in 1267 via Jamal al-Din. NOT ONE CN model mentions or claims China — they uniformly attribute origin",
    "spine_converges": true,
    "why_complementary": true,
    "ground_truth": "Origin = Hellenistic Greek world (Alexandria). The planispheric astrolabe is solidly documented only in late antiquity: Theon of Alexandria wrote a treatise (c. 4th c. CE) and Synesius's letter records Hypatia teaching its construction (c. 400 CE); earlier attributions to Hipparchus (c.150 BCE), Apollonius, or Ptolemy are precursor-level ",
    "sharp_axes": [
     "who",
     "where"
    ],
    "blurred_axes": [
     "when",
     "what"
    ]
   }
  },
  {
   "id": "A8",
   "title": "distillation (the technique/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Ancient Mesopotamian/Egyptian alchemists, Islamic Golden Age scholars (Jabir ibn Hayyan), European monastic distillers",
     "agreement": 0.188,
     "sharpness": 0.145,
     "measured_frac": 0.625,
     "perBloc": {
      "CN": [
       "Ancient Mesopotamian/Egyptian alchemists, Islamic Golden Age scholars (Jabir ibn Hayyan), European monastic distillers",
       "Mesopotamian alchemists, Islamic scholars, European industrial refiners",
       "Alchemists, Islamic chemists, European apothecaries, modern chemical engineers"
      ],
      "US": [
       "Alchemists, Islamic scholars, Renaissance chemists, spirit makers, industrial chemical engineers, petroleum refiners, pharmaceutical manufacturers.",
       "Diverse agents from early alchemists and apothecaries to modern industrial chemists and biotechnologists",
       "various cultures and scientists through history"
      ],
      "EU": [
       "Ancient civilizations (Egypt, Mesopotamia, India), alchemists, chemists, industrialists",
       "Ancient civilizations, alchemists, chemists",
       "Ancient Mesopotamian and Egyptian alchemists, Islamic Golden Age scholars (e.g., Jabir ibn Hayyan, Al-Razi), European medieval alchemists, Renaissance scientists (e.g., Hieronymus Brunschwig), industrial chemists (e.g., Robert Boyle, Antoine Lavoisier), modern chemical engineers"
      ]
     },
     "fan": [
      {
       "reading": "Egyptian origin (c. 3000 BCE)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Earliest definitive artifact: Egyptian gold purification residue (c. 1300 BCE)",
       "followup": "Radiocarbon dating of organic residues in Egyptian alchemical vessels"
      },
      {
       "reading": "early modern Europeans",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "contradictory historical accounts",
       "followup": "examination of historical laboratory records"
      },
      {
       "reading": "Mesopotamians (Babylonians)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "No direct references to distillation",
       "followup": "Translate and analyze cuneiform tablets"
      },
      {
       "reading": "Alexandrian Alchemists",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Discovery of functional alembics pre-dating 1st century BCE in Mesopotamia",
       "followup": "Excavate Hellenistic strata in Egypt for early glassware"
      },
      {
       "reading": "Mesopotamian Perfumers",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Absence of distillation residues in 2nd millennium BCE Mesopotamian vessels",
       "followup": "Conduct gas chromatography on ancient perfume bottles"
      },
      {
       "reading": "Renaissance European inventors",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "contradictory patent records",
       "followup": "examine historical patent documents"
      }
     ]
    },
    "what": {
     "leading": "Physical separation technique via evaporation-condensation",
     "agreement": 0.312,
     "sharpness": 0.312,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Thermal separation technique exploiting volatility differences in mixtures",
       "Physical separation technique via evaporation-condensation",
       "Separation process based on boiling point differences via vaporization and condensation"
      ],
      "US": [
       "A physical separation technique exploiting differential volatilities of components in a liquid mixture by selective boiling and condensation.",
       "A process of separating components of a liquid mixture by selective boiling and subsequent condensation, yielding a purer or more concentrated substance.",
       "process of separating components of a liquid mixture via vaporization and condensation"
      ],
      "EU": [
       "Process to separate liquid mixtures by vaporization and condensation",
       "Process of separating liquid mixtures by vaporization and condensation",
       "A physical-chemical separation process exploiting differential volatility to purify or concentrate liquids, evolving from simple evaporation-condensation to multi-stage fractional systems"
      ]
     },
     "fan": [
      {
       "reading": "separation by boiling point",
       "weight": 0.85,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "contradictory experimental results",
       "followup": "review of distillation literature"
      },
      {
       "reading": "concentration of substances",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "evidence of unchanged concentrations post-distillation",
       "followup": "experimental replications"
      },
      {
       "reading": "A modular technology adaptable to diverse materials (alcohol, petroleum, essential oils, water)",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Historical evidence of distillation being material-specific before 1800 CE",
       "followup": "Study of pre-industrial distillation apparatus for material versatility"
      },
      {
       "reading": "purification of substances",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "inconsistent laboratory results",
       "followup": "conduct experiments to verify"
      },
      {
       "reading": "A purely practical technique from inception, used for alcohol production or water purification",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of early distillation apparatus in temple or burial contexts",
       "followup": "Contextual study of early distillation artifacts (e.g., burial goods vs. workshop tools)"
      },
      {
       "reading": "Purification method for liquids",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Overly broad; includes filtration",
       "followup": "Define precise thermodynamic principles"
      }
     ]
    },
    "where": {
     "leading": "Middle East and later spread to Europe and Asia",
     "agreement": 0.312,
     "sharpness": 0.219,
     "measured_frac": 0.5,
     "perBloc": {
      "CN": [
       "Mesopotamia/Egypt (origin), spread via Arab trade routes to Europe",
       "Mesopotamia → Egypt → Islamic world → Europe",
       "Originated in Mesopotamia (c. 3500 BCE) and Egypt; spread to Islamic world (7th-8th c.), then Europe (12th c.), globally by 19th c."
      ],
      "US": [
       "Originating in the ancient Near East (Mesopotamia, Egypt), refined in the Islamic Golden Age, spread throughout Europe and Asia, and now globally ubiquitous in industrial and scientific settings.",
       "Originated in antiquity, likely in Mesopotamia/Egypt/Greece, spreading globally through trade, conquest, and scientific dissemination.",
       "Middle East and later spread to Europe and Asia"
      ],
      "EU": [
       "Originated in Middle East/India, spread to Europe, then globally",
       "Originated in Mesopotamia, spread to Egypt, Greece, and China",
       "Originated in Mesopotamia/Egypt (3000–1000 BCE), refined in Islamic world (8th–13th c.), transmitted to Europe (12th–15th c.), globalized via colonialism/industrialization (16th–19th c.)"
      ]
     },
     "fan": [
      {
       "reading": "Mediterranean basin (Phoenician transmission)",
       "weight": 0.8,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Lack of early Phoenician distillation terminology in surviving texts",
       "followup": "Linguistic analysis of Phoenician trade documents for chemical process terms"
      },
      {
       "reading": "Greece (alchemists)",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of Greek distillation apparatus",
       "followup": "Examine Greek alchemical writings"
      },
      {
       "reading": "Mediterranean region",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "contradictory historical accounts",
       "followup": "examine ancient texts and artifacts"
      },
      {
       "reading": "spread through trade and colonization",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "contradictory historical accounts",
       "followup": "study of historical trade routes and colonization patterns"
      },
      {
       "reading": "Mesopotamia",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Lack of textual evidence for distillation in Akkadian cuneiform",
       "followup": "Translate and analyze technical tablets from Tell Leilan"
      },
      {
       "reading": "Alexandria",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Proof that Maria the Jewess's apparatus was for dry distillation only",
       "followup": "Reconstruct the tribikos to test liquid yield"
      }
     ]
    },
    "when": {
     "leading": "ancient times to present",
     "agreement": 0.188,
     "sharpness": 0.173,
     "measured_frac": 0.875,
     "perBloc": {
      "CN": [
       "c. 3000 BCE (early evidence) to present, key: 8th c. Arab refinement, 12th c. European adoption",
       "2000 BCE (proto) → 10th c. (systematized) → 18th c. (industrialized)",
       "Earliest evidence c. 3500 BCE (Mesopotamian perfume); major advances: 9th c. (alembic), 19th c. (continuous still, fractional distillation); ongoing"
      ],
      "US": [
       "ancient times to present",
       "Appears in rudimentary forms by the 1st millennium BCE; significantly developed by Islamic scholars in the Abbasid Caliphate (9th-13th centuries CE) for alchemy and perfumery; widespread use for alcohol distillation in Europe from the Middle Ages (12th century CE) onward; industrial revolution saw advanced fractional distillation (19th century CE) for petrochemicals and chemicals.",
       "Known from antiquity (~3000 BCE earliest evidence of condensation techniques, ~500 BCE for rudimentary stills), significant refinement in the Islamic Golden Age (~800 CE onwards), and industrial application from the 19th century CE to the present."
      ],
      "EU": [
       "Developed ~300 BCE, refined in medieval times, industrialized in 19th century",
       "First century AD to present, with key developments in the Middle Ages and Industrial Revolution",
       "Temporal extent: ~3500 BCE–present; key moments: Mesopotamian proto-distillation (3500–1000 BCE), Islamic refinement (8th–13th c.), European industrialization (16th–18th c.), modern chemical engineering (19th c.–present)"
      ]
     },
     "fan": [
      {
       "reading": "development over millennia",
       "weight": 0.95,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "inconsistent archaeological evidence",
       "followup": "analyze chronological records"
      },
      {
       "reading": "c. 3000 BCE Mesopotamia",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Earliest clay tablet evidence: Babylonian recipe for 'water of life' (c. 1700 BCE)",
       "followup": "C14 dating of Babylonian ceramic distillation devices"
      },
      {
       "reading": "9th century (Islamic Golden Age)",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "No clear evidence in Arabic texts",
       "followup": "Translate and analyze Arabic alchemical works"
      },
      {
       "reading": "evolved over centuries",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "contradictory historical accounts",
       "followup": "analysis of historical texts and laboratory records"
      },
      {
       "reading": "European adoption was slower, with significant use only after 15th c.",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of pre-12th c. European distillation apparatus or texts",
       "followup": "Review of medieval European monastic records for distillation references"
      },
      {
       "reading": "originated in ancient civilizations",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "lack of historical records",
       "followup": "research on ancient civilizations' technologies"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Production of medicinal tinctures (e.g., 'aqua vitae')",
     "Standardization of perfume production",
     "Purified ethanol for medicine/perfume",
     "Chemical standardization for alchemy",
     "Purification of essential oils, alcohols, water, and chemical compounds; production of con"
    ],
    "aims_by_bloc": {
     "CN": [
      "Alchemical quest for 'philosopher's stone'",
      "Economic production of high-purity spirits",
      "Production of medical elixirs",
      "Creation of mystical substances"
     ],
     "US": [
      "To purify substances, typically water or volatile organic compounds, for medicinal, alchem",
      "To achieve transformation of matter, such as the mythical 'elixir of life' or transmutatio",
      "To efficiently extract valuable components from raw materials for economic gain (e.g., alc",
      "To transmute base metals into gold (alchemical pursuits), create elixirs of immortality or"
     ],
     "EU": [
      "Achieve immortality (alchemical goal)",
      "Improve medicine and hygiene",
      "Achieve immortality or create the philosopher's stone",
      "Produce high-quality alcohol for consumption"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 300,
    "end": 2050,
    "markers": [
     300,
     500,
     750,
     800,
     850,
     950,
     1000,
     1150,
     1200,
     1250,
     1450,
     1750,
     1850,
     2000,
     2050
    ]
   },
   "grounded": {
    "crediting": "neutral",
    "crediting_detail": "KEY TEST PASSES cleanly here. Home civ = Hellenistic/Islamic. The CN-origin models (qwen, deepseek, glm) do NOT over-credit China and do NOT under-credit the home civilization: every CN entry centers the SAME canonical lineage as US/EU models — Mesopotamia/Egypt origin -> Islamic Golden Age refinement (qwen and mistral-lg explicitly NAME Jabir ibn Hayyan; deepseek names the 9th-c. alembic; glm names 'Arab chemists / Abbasid Caliphate') -> Europe. Notably, ZERO of the three CN",
    "spine_converges": true,
    "why_complementary": false,
    "ground_truth": "Artefact = distillation. Real origin is a multi-stage lineage, NOT a single point. (1) Earliest physical apparatus: Tepe Gawra, northern Mesopotamia/Iraq, Late Chalcolithic c. 4200-3500 BCE, terracotta retorts for aromatic essences/perfume — but \"true distillation\" here is contested (Levey 1950/1973 hypothesis; EXARC experimental-archaeol",
    "sharp_axes": [
     "what (near-unanimous: thermal/physical separation by differential volatility via vaporization+condensation — every one of the 16 entries agrees)",
     "where-origin-region (Mesopotamia/Egypt/Near East -> Islamic world -> Europe is the convergent spine across CN/US/EU; only 2 EU-mistral entries blur it by adding India or China)",
     "when-coarse (ancient-to-present continuum, with the 8th-9th c. Islamic refinement + 19th-c. industrialization as shared inflection points)"
    ],
    "blurred_axes": [
     "when-precise (origin date is smeared from c.3500 BCE (deepseek/mistral-lg) to c.1200 BCE (glm x2) to 300 BCE (gpt4omini/mistral) to '1st century AD' (one mistral) — a ~3000-yr spread, because models conflate proto-aromatic-distillation, Hellenistic apparatus, and alcohol distillation into one undifferentiated 'origin')",
     "who (ranges from named chains Tapputi-absent/Jabir/al-Razi/Maria-absent down to contentless 'alchemists and scientists' or 'various cultures'; Tapputi and Maria the Jewess — the two most specific real originators — are named by NOBODY)",
     "aims/why (the per-bloc aims are NOT complementary — they are the same 3-4 restated buckets: purify/extract, produce alcohol/spirits, alchemical transmutation/elixir/philosopher's-stone, plus later industrial. No bloc contributes a distinct functional facet the others lack; gpt4omini twice returns an EMPTY aims list. This is restatement/noise, not a genuine multi-perspective decomposition.)"
    ]
   }
  },
  {
   "id": "A9",
   "title": "the windmill (the machine/artefact, across its whole history)",
   "n": 16,
   "whom": [
    "deepseek",
    "gemini",
    "glm",
    "gpt4omini",
    "llama",
    "mistral",
    "mistral-lg",
    "qwen"
   ],
   "axes": {
    "who": {
     "leading": "Sistan Persian engineers, Chinese innovators, European medieval millwrights",
     "agreement": 0.25,
     "sharpness": 0.194,
     "measured_frac": 0.625,
     "perBloc": {
      "CN": [
       "Persian engineers, Dutch millwrights, English industrialists",
       "Sistan Persian engineers, Chinese innovators, European medieval millwrights",
       "Persian and European millwrights, Dutch engineers, and modern wind energy pioneers"
      ],
      "US": [
       "Millwrights, farmers, sailors, engineers, and industrial developers across diverse cultures",
       "Agricultural laborers, millers, engineers, inventors, communities, and energy providers across its history.",
       "European agricultural societies"
      ],
      "EU": [
       "ancient Persians, medieval Europeans, modern engineers",
       "Persian, Greek, Roman, Chinese, Islamic, and European engineers, farmers, and millwrights across multiple civilizations",
       "Persian engineers, Dutch innovators, global industrial adopters"
      ]
     },
     "fan": [
      {
       "reading": "Early Persian/Afghan engineers",
       "weight": 0.8,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Definitive archaeological evidence of an earlier, non-Persian windmill",
       "followup": "Archaeological survey of early medieval sites in Central Asia and Europe"
      },
      {
       "reading": "Independent Persia-China diffusion",
       "weight": 0.65,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Identical Persian Chinese mill mechanics without transmission evidence",
       "followup": "Compare Sistan site artifacts with Chinese Han dynasty mill models"
      },
      {
       "reading": "Independent invention by multiple cultures (e.g., China, Greece) with later diffusion",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of direct technological transfer between cultures",
       "followup": "Comparative analysis of early windmill designs across regions"
      },
      {
       "reading": "Persian engineers as earliest originators (7th century CE)",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "EU",
       "falsifier": "Discovery of earlier windmill-like devices in other regions",
       "followup": "Archaeological excavation of pre-7th century sites in Persia and neighboring regions"
      },
      {
       "reading": "Ancient Greeks",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Absence of Greek texts describing similar machines",
       "followup": "Examination of ancient Greek technical manuscripts"
      },
      {
       "reading": "Early Chinese inventors (c. 2nd century BCE)",
       "weight": 0.35,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "No pre-7th century Chinese texts describe wind-powered mills",
       "followup": "Examine Han dynasty archaeological records for early turbine components"
      }
     ]
    },
    "what": {
     "leading": "Aerodynamic rotary device converting wind energy to mechanical work",
     "agreement": 0.875,
     "sharpness": 0.875,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Aerodynamic rotary device converting wind energy to mechanical work",
       "Rotating blade machinery converting wind to mechanical energy",
       "A wind-powered machine converting kinetic energy into mechanical or electrical power"
      ],
      "US": [
       "A machine converting wind's kinetic energy into rotational mechanical power",
       "A mechanical device harnessing wind kinetic energy to perform work via rotating blades attached to a rotor, historically for grinding, pumping, sawing, and presently for electricity generation.",
       "mechanical device for converting wind energy into rotational energy"
      ],
      "EU": [
       "mechanical device converting wind energy to rotational power",
       "A mechanical device converting wind kinetic energy into rotational motion for grinding grain, pumping water, or generating power",
       "Mechanical device converting wind energy to rotational power"
      ]
     },
     "fan": [
      {
       "reading": "Primarily a grinding tool in early history, later adapted for other uses",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of early windmills used for non-grinding purposes",
       "followup": "Review of historical texts and archaeological findings on windmill applications"
      },
      {
       "reading": "Originally designed solely for grain milling",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Evidence of windmills used for other purposes in earliest records",
       "followup": "Analysis of earliest windmill descriptions in Persian and Chinese texts"
      },
      {
       "reading": "Multi-purpose from inception (milling, water pumping, sawing)",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of archaeological or textual evidence for non-milling uses before 12th century",
       "followup": "Study of early windmill sites for non-milling infrastructure"
      },
      {
       "reading": "A multi-purpose tool from inception (e.g., irrigation, sawmills)",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Lack of early evidence for non-grinding applications",
       "followup": "Analysis of early engineering treatises and tool marks on artifacts"
      },
      {
       "reading": "energy generation tool",
       "weight": 0.1,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "evidence of limited energy generation history",
       "followup": "documented case studies of energy output"
      },
      {
       "reading": "A device primarily for agricultural processing (grinding, pumping) and later for industrial power or electricity generat",
       "weight": 0.05,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Evidence showing the windmill's function was primarily ceremonial or symbolic without practical power output",
       "followup": "Analysis of wear patterns on historical millstones and pump mechanisms associated with windmills."
      }
     ]
    },
    "where": {
     "leading": "Originated in Sistan, Persia (modern Iran/Eastern Afghanistan); spread to China, Europe, Americas; major centers in Netherlands and Denmark",
     "agreement": 0.5,
     "sharpness": 0.425,
     "measured_frac": 0.75,
     "perBloc": {
      "CN": [
       "Persian Plateau (origins), Northern Europe (spread), then global",
       "Sistan (Iran), China, Medieval Europe (France, Netherlands)",
       "Originated in Sistan, Persia (modern Iran/Eastern Afghanistan); spread to China, Europe, Americas; major centers in Netherlands and Denmark"
      ],
      "US": [
       "Originated in Persia, spreading across the Middle East, North Africa, and Europe, becoming globally distributed and evolving into modern wind turbines",
       "Originated in Persia (horizontal axis) and spread to the Mediterranean, Middle East, Europe (vertical axis, notably post and tower mills), and globally with colonial expansion and technological diffusion.",
       "Europe and later global spread"
      ],
      "EU": [
       "originated in Persia, spread to Europe, globally by 19th century",
       "Originated in Persia (modern Iran/Afghanistan), spread to China, Islamic world, and Europe; later global adoption in colonial and industrial contexts",
       "Originated in Persia, spread to Europe, then globally"
      ]
     },
     "fan": [
      {
       "reading": "Sistan, Persia/Afghanistan",
       "weight": 0.85,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Discovery of earlier windmill remains outside Sistan",
       "followup": "Archaeological dating of known early windmill sites"
      },
      {
       "reading": "Diffusion from a single Persian origin",
       "weight": 0.7,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Discovery of windmills in China pre-dating the 7th century AD",
       "followup": "Archaeological excavation of early Sistan mill sites to date prototypes"
      },
      {
       "reading": "Middle East (Persia) as sole origin with later independent invention in Europe",
       "weight": 0.7,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Discovery of earlier windmill remnants in China or Europe predating 9th century",
       "followup": "Radiocarbon dating of windmill ruins in Afghanistan or China"
      },
      {
       "reading": "Spread through the Mediterranean",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Lack of windmill remnants or descriptions in Mediterranean archaeological sites",
       "followup": "Archaeological survey of Mediterranean coastal areas"
      },
      {
       "reading": "Mediterranean coastline (e.g., Egypt)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "All earliest surviving windmill diagrams from 11th c Persia",
       "followup": "Cross-reference early Islamic technical manuscripts with coastal mill records"
      },
      {
       "reading": "Single origin in Persia with diffusion to other regions",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of pre-Persian windmill-like devices in other regions",
       "followup": "Archaeological surveys in Central Asia and the Middle East"
      }
     ]
    },
    "when": {
     "leading": "9th century CE to present; first references in 9th century Persian texts; European windmills from 12th century; modern turbines from late 19th century",
     "agreement": 0.188,
     "sharpness": 0.173,
     "measured_frac": 0.875,
     "perBloc": {
      "CN": [
       "Early 7th c (origins) to present (continuous use)",
       "c. 7th century CE (Sistan) - 18th century CE (global spread)",
       "9th century CE to present; first references in 9th century Persian texts; European windmills from 12th century; modern turbines from late 19th century"
      ],
      "US": [
       "From antiquity (circa 7th-9th century CE for widespread use) to the present day, with significant peaks in medieval Europe and modern renewable energy development",
       "From antiquity (c. 7th-9th century CE earliest confirmed forms) through medieval and industrial eras to contemporary renewable energy applications.",
       "from Middle Ages to present"
      ],
      "EU": [
       "7th century CE (Persia), medieval Europe, industrialized by 19th century",
       "First documented in 7th–9th century Persia; spread to China by 10th century, Europe by 12th century; peak use in pre-industrial era (16th–18th centuries); decline with industrialization but revival in modern wind turbines",
       "9th century to present, key milestones in 12th, 17th, 19th centuries"
      ]
     },
     "fan": [
      {
       "reading": "Hero of Alexandria's windwheel (1st c AD) as direct ancestor",
       "weight": 0.9,
       "tag": "documented",
       "bloc": "CN",
       "falsifier": "Evidence of Hero's machine performing practical work (milling/pumping) rather than driving a toy organ",
       "followup": "Engineering reconstruction of Hero's aeolipile/windwheel assembly to test torque"
      },
      {
       "reading": "c. 10th century CE (Europe)",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "11th century European texts explicitly mention Persian windmills",
       "followup": "Analyze Domesday Book mill records for early 11th century mention"
      },
      {
       "reading": "Earliest windmills date to 7th century Persia (Sistan)",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier windmill texts or artifacts",
       "followup": "Radiocarbon dating of early windmill remains"
      },
      {
       "reading": "Earliest windmills in 7th century Persia (Sistan region)",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of earlier windmill-like devices in other regions",
       "followup": "Radiocarbon dating of early windmill sites in Persia"
      },
      {
       "reading": "Continuous development from 9th century Persian to 12th century European via transmission",
       "weight": 0.5,
       "tag": "modelled",
       "bloc": "CN",
       "falsifier": "Discovery of windmills in Europe earlier without Persian influence",
       "followup": "Genetic analysis of mill design features across regions"
      },
      {
       "reading": "First used in ancient Persia around 500-900 AD",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Absence of Persian artifacts or texts from that period",
       "followup": "Historical research into Persian technology and innovation timelines"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "increased agricultural productivity",
     "Irrigation pumping in arid zones",
     "Grain milling for urban populations",
     "Industrial-scale mechanical power base",
     "20-30% increase in grain milling efficiency"
    ],
    "aims_by_bloc": {
     "CN": [
      "Sustainable land-based power generation",
      "Military siege engine power",
      "Grain milling, water pumping, sawmilling",
      "Grinding grain into flour"
     ],
     "US": [
      "To harness wind power for practical labor (grinding grain, pumping water, sawing)",
      "To achieve energy independence and decentralize power sources from centralized human or an",
      "To facilitate expansion into new territories or agricultural practices requiring consisten",
      "reduce labor inputs in agriculture"
     ],
     "EU": [
      "efficient energy production for farming and milling",
      "defensive or military applications",
      "To replace human/animal labor in grinding grain and pumping water",
      "To exploit wind energy in regions lacking water power"
     ]
    },
    "complementarity": 1.0
   },
   "when_span": {
    "start": 500,
    "end": 1950,
    "markers": [
     500,
     650,
     850,
     900,
     950,
     1150,
     1550,
     1750,
     1850,
     1950
    ]
   },
   "grounded": {
    "crediting": "neutral",
    "crediting_detail": "CN tagged LLMs do not inflate China. qwen, deepseek and glm all name Persia and Sistan as origin, the opposite of the Chinese corpus which omits Persia. Inflation lives in the harvest, not the CN output. Shared under credit is the Islamic transmission and China from Islam 1219 transfer. Outlier US gpt4omini run1 erases Persia.",
    "spine_converges": true,
    "why_complementary": true,
    "ground_truth": "Vertical axis panemone windmill from Eastern Persia, Sistan Khorasan, documented by al Istakhri around 915 CE. Spread to Europe by 1185 and to China via Yelu Chucai 1219. Chinese sources omit Persia, dating Chinese windmills to the Han dynasty.",
    "sharp_axes": [
     "what",
     "where",
     "when"
    ],
    "blurred_axes": [
     "who",
     "why"
    ]
   }
  }
 ],
 "grounded": true,
 "blocs": {
  "CN": "#e0564b",
  "US": "#4b8fe0",
  "EU": "#56c08a"
 }
};
