const SUBSTRATE = {
 "source": "substrate_probe_run.jsonl",
 "n_records": 48,
 "n_parsed": 44,
 "artefacts": [
  {
   "id": "E1",
   "title": "movable-type printing (the technology/artefact itself, across its whole history)",
   "n": 14,
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
     "leading": "Bi Sheng, Johannes Gutenberg, and later refiners/printers",
     "agreement": 0.429,
     "sharpness": 0.373,
     "measured_frac": 0.786,
     "perBloc": {
      "US": [
       "Humanity's collective efforts in knowledge dissemination",
       "Diverse innovators, craftsmen, and institutions across Song Dynasty China, Goryeo Korea, and Renaissance Europe",
       "multi-agent"
      ],
      "CN": [
       "Chinese/Korean artisans, Johannes Gutenberg, European printers",
       "Johannes Gutenberg, Andreas Heilmann, Johann Fust, Peter Schoeffer, Chinese/Middle Eastern innovators (pre-1400s), European printers (15th-20th centuries)",
       "Printers, typefounders, publishers, religious reformers, state bureaucrats, and scholars"
      ],
      "EU": [
       "Bi Sheng, Johannes Gutenberg, and later refiners/printers",
       "Bi Sheng (originator, 11th c.), Johannes Gutenberg (refiner, 15th c.), European printers (transmitters), global publishers (notable users)",
       "Bi Sheng (originator, 11th c. China), Johannes Gutenberg (refiner, 15th c. Europe), Korean artisans (transmitters, 13th-14th c.), European printers (notable users, 15th-16th c.)"
      ]
     },
     "fan": [
      {
       "reading": "Gutenberg as sole European originator (c.1440)",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Discovery of pre-Gutenberg European type fragments",
       "followup": "Analyze 14th-century manuscript margins for printing-related marks"
      },
      {
       "reading": "Gutenberg as sole originator (1440s Mainz)",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Documentary evidence of prior movable-type use in Asia/Cyprus",
       "followup": "Examine 14th-century Chinese/Armenian printing records for type use"
      },
      {
       "reading": "Johannes Gutenberg and his immediate predecessors/successors in 15th Century Europe",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Overwhelming evidence that Gutenberg's invention was directly and significantly inspired or copied from East Asian systems without attribution.",
       "followup": "Detailed financial and technical audits of Gutenberg's workshop and his sources of inspiration."
      },
      {
       "reading": "Korean artisans as primary innovators (post-1230)",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No extant Korean type or documentation predating 1230",
       "followup": "Locate 13th-century Korean printing records showing movable type"
      },
      {
       "reading": "Collaborative German workshop (Fust & Schoeffer after Gutenberg)",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Gutenberg's 1430s technical patents",
       "followup": "Analyze Nuremberg court documents on Gutenberg's 1439 lawsuit"
      },
      {
       "reading": "Gutenberg",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "earlier printing evidence",
       "followup": "investigate 12th-century China"
      }
     ]
    },
    "what": {
     "leading": "System of reusable metal type characters for printing",
     "agreement": 0.143,
     "sharpness": 0.143,
     "measured_frac": 1.0,
     "perBloc": {
      "US": [
       "A system of reusable, individual character-molds for mechanical replication of text and images.",
       "A system employing individual, reusable type characters cast from metal, ceramic, or wood, set in a frame, inked, and pressed onto a surface, facilitating mass duplication of texts.",
       "metal type casting"
      ],
      "CN": [
       "System of reusable metal type characters for printing",
       "Movable metal type, ink, and press system for high-volume text reproduction",
       "A system of replicating text using reusable, matrix-cast type elements arranged in a press"
      ],
      "EU": [
       "A printing technology using movable metal/ceramic type pieces",
       "A printing system using reusable metal or ceramic type pieces",
       "Modular system of reusable, rearrangeable characters for printing text, enabling mass production of written material"
      ]
     },
     "fan": [
      {
       "reading": "A catalyst for standardization of language and script",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Lack of correlation between printing centers and linguistic uniformity",
       "followup": "Linguistic mapping of dialect shifts pre/post-printing"
      },
      {
       "reading": "A modular system for rapid text reproduction, adaptable to multiple scripts (e.g., Latin, Hanzi)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of non-modular or script-specific limitations in early implementations",
       "followup": "Comparative study of typefaces across cultures"
      },
      {
       "reading": "Primarily a tool for religious propaganda (e.g., Bibles, sutras)",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of early secular or commercial uses dominating output",
       "followup": "Quantitative analysis of earliest printed materials by genre"
      },
      {
       "reading": "Primarily a tool for religious proselytization (early phase)",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of secular texts dominating early print runs",
       "followup": "Quantitative analysis of incunabula content"
      },
      {
       "reading": "Specifically metal type with oil-based ink and screw press",
       "weight": 0.2,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "Ceramic and wooden movable type exist earlier and are still movable-type printing",
       "followup": "Examine material compositions of early type specimens"
      },
      {
       "reading": "wooden type",
       "weight": 0.1,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "metal type dominance evidence",
       "followup": "examine early presses"
      }
     ]
    },
    "where": {
     "leading": "Originated in East Asia (China, Korea), popularized and refined in Europe (Germany), and spread globally.",
     "agreement": 0.286,
     "sharpness": 0.261,
     "measured_frac": 0.857,
     "perBloc": {
      "US": [
       "Originated in East Asia (China, Korea), popularized and refined in Europe (Germany), and spread globally.",
       "Originated in Song Dynasty China and Goryeo Korea, popularized and technologically refined in Europe, and subsequently spread globally.",
       "Eurasia"
      ],
      "CN": [
       "East Asia (China/Korea) → Europe (Mainland and Germanic regions)",
       "Mainz (origin), spread across Europe (Venice, Paris, Antwerp), then global",
       "East Asia (China/Korea) and Europe"
      ],
      "EU": [
       "Originated in China (11th century), spread to Europe (15th century)",
       "Originated in China (11th century), spread to Korea, and later to Europe (15th century)",
       "Originated in China (11th c.), refined in Korea (13th–14th c.), revolutionized in Europe (15th c.), spread globally via colonialism and trade (16th–19th c.)"
      ]
     },
     "fan": [
      {
       "reading": "Central Asian relay via Mongol Empire (13th-14th c.)",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Absence of Mongol-era type artifacts along Silk Road routes",
       "followup": "Excavate 13th-century trading hubs for early movable type fragments"
      },
      {
       "reading": "Originated in Mainz, Germany",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Evidence of earlier similar techniques in other regions",
       "followup": "Exploration of archaeological findings"
      },
      {
       "reading": "Independent reinvention in Europe (15th c.)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of pre-Gutenberg European movable-type artefacts",
       "followup": "Metallurgical analysis of early European type to trace origins"
      },
      {
       "reading": "Mainz, Germany (c. 1439-1440s) as sole origin",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Archaeological evidence of identical technology in China (c. 1200s)",
       "followup": "Verify 12th-century Chinese metal type fragments from Dingzhou"
      },
      {
       "reading": "Mainz, with Chinese precursor influence (e.g., via Mongol trade routes)",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Absence of verified Chinese movable-type in 15th-century German records",
       "followup": "Cross-reference Song Dynasty printing documents with Cologne archives"
      },
      {
       "reading": "Europe",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "non-European early adoption",
       "followup": "investigate Silk Road"
      }
     ]
    },
    "when": {
     "leading": "11th century (China) to present, with key developments in 15th century (Europe)",
     "agreement": 0.286,
     "sharpness": 0.286,
     "measured_frac": 1.0,
     "perBloc": {
      "US": [
       "Early 11th century (earliest ceramic type) to late 20th century (peak industrial phase), with conceptual remnants still present.",
       "First developed circa 11th century in China, with key advancements by the 13th century in Korea, and revolutionary widespread adoption and refinement in Europe from the mid-15th century onwards.",
       "15th-20th centuries"
      ],
      "CN": [
       "11th c. (China) → 13th c. (Korea) → 1440s (Europe) → 16th+ c. (global spread)",
       "1430s (Mainz) → 1500s (Europe) → 1600s+ (global spread)",
       "11th century (Song Dynasty) to present"
      ],
      "EU": [
       "11th century (China) to present, with key developments in 15th century (Europe)",
       "11th century (China) to present, with key milestones in 15th-century Europe",
       "1040s (Bi Sheng’s clay type) to present (digital transition), with key moments: 1234 (Korean metal type), 1450s (Gutenberg’s press), 1814 (steam-powered press), 1980s (desktop publishing)"
      ]
     },
     "fan": [
      {
       "reading": "Rise began in 1450s with Gutenberg",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Evidence of functional printing before Gutenberg",
       "followup": "Verification of earlier European printing efforts"
      },
      {
       "reading": "Continued relevance through modern digital adaptation",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Decline in physical print media usage",
       "followup": "Statistical analysis of print media consumption trends"
      },
      {
       "reading": "Earlier Chinese prototypes (pre-1040s)",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "No archaeological evidence of pre-1040 movable type",
       "followup": "Excavations at Song Dynasty printing sites"
      },
      {
       "reading": "Earliest movable type predates 11th c. in China",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Discovery of pre-11th c. Chinese type or unambiguous references",
       "followup": "Systematic review of Tang Dynasty texts for printing references"
      },
      {
       "reading": "A technology whose impact was confined to a few centuries before obsolescence.",
       "weight": 0.1,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Documentation of continuous use, adaptation, and influence of printing principles beyond the industrial era.",
       "followup": "Analysis of print-based media's role in the information age preceding widespread digital adoption."
      },
      {
       "reading": "earlier origins",
       "weight": 0.1,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "definitive 15th-century origin proof",
       "followup": "examine ancient civilizations"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Mass proliferation of literacy and knowledge.",
     "Standardization of languages and orthography.",
     "Acceleration of scientific discovery and philosophical dissemination.",
     "Empowerment of dissent and political movements.",
     "Accelerated the spread of knowledge, facilitated major intellectual and religious movement"
    ],
    "aims_by_bloc": {
     "US": [
      "To replicate religious texts accurately and widely.",
      "To facilitate administration and bureaucracy.",
      "To profit from the sale of books and information.",
      "To increase the speed and reduce the labor cost of reproducing written materials."
     ],
     "CN": [
      "Religious propagation (Christian/Confucian)",
      "Bureaucratic standardization (e.g., legal codes)",
      "Accelerating religious reform and dissemination of vernacular texts",
      "Centralizing state-controlled information (e.g., papal decrees)"
     ],
     "EU": [
      "Standardize religious texts",
      "Profit from book sales",
      "To spread religious texts and ideologies",
      "To standardize and preserve knowledge"
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
     1350,
     1450,
     1814,
     1850,
     1950
    ]
   }
  },
  {
   "id": "E2",
   "title": "gunpowder (the substance/artefact itself, across its whole history)",
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
     "leading": "Chinese alchemists, Song military, Mongol disseminators, European gunsmiths",
     "agreement": 0.438,
     "sharpness": 0.421,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "Chinese alchemists",
       "Chinese alchemists (Tang dynasty), Mongols (transmission), European artillery makers (refinement)",
       "Chinese alchemists, Song military, Mongol disseminators, European gunsmiths"
      ],
      "US": [
       "Chinese alchemists, Arab traders, Mongol armies, European military engineers, and global military forces",
       "Diverse agents across East Asia, the Middle East, and Europe, from alchemists to state armies and industrialists",
       "Chinese alchemists, European chemists, military leaders"
      ],
      "EU": [
       "Chinese alchemists, European military engineers, global industrialists",
       "Chinese alchemists, European chemists, military strategists, industrial manufacturers",
       "Chinese alchemists (originators), Song Dynasty military engineers (refiners), Mongol transmitters, European and Islamic military adopters (notable users)"
      ]
     },
     "fan": [
      {
       "reading": "Chinese alchemists",
       "weight": 0.6,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "no contemporary records",
       "followup": "archaeological excavation in Chinese historic sites"
      },
      {
       "reading": "Chinese Daoist alchemists (9th century)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "No pre-9th century Chinese records of gunpowder",
       "followup": "Examine Tang Dynasty alchemical texts for earlier references"
      },
      {
       "reading": "Song dynasty military engineers (primary authors)",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No pre-12th c. Song military texts detailing gunpowder use",
       "followup": "Analyze Tang-era alchemical manuscripts in Dunhuang caves"
      },
      {
       "reading": "Middle Eastern traders",
       "weight": 0.4,
       "tag": "modelled",
       "bloc": "US",
       "falsifier": "no trade route evidence",
       "followup": "historical trade route analysis"
      },
      {
       "reading": "Chinese alchemists (Taoist tradition) as sole originators",
       "weight": 0.4,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of pre-Chinese gunpowder-like compounds in other regions",
       "followup": "Archaeochemical analysis of pre-9th century residues in Central Asia or India"
      },
      {
       "reading": "Mongol transmission network (primary vector only)",
       "weight": 0.35,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Documented Chinese gunpowder manuals before Mongol conquest",
       "followup": "Trace earliest Middle Eastern gunpowder recipes to Chinese sources"
      }
     ]
    },
    "what": {
     "leading": "Potassium nitrate, sulfur, charcoal mixture",
     "agreement": 0.875,
     "sharpness": 0.875,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Potassium nitrate, sulfur, charcoal mixture",
       "Nitrate-sulfur-charcoal mixture (75-10-15 ratio) used as propellant/explosive",
       "Mixture of saltpeter (KNO3), sulfur, and charcoal; deflagrates producing gas"
      ],
      "US": [
       "A highly combustible mixture of saltpeter, sulfur, and charcoal, used as a propellant and explosive agent.",
       "A ternary mixture of sulfur, charcoal, and saltpeter (potassium nitrate), functioning primarily as a propellant and explosive",
       "explosive mixture of saltpeter, sulfur, and charcoal"
      ],
      "EU": [
       "Explosive mixture of saltpeter, sulfur, and charcoal",
       "Mixture of saltpeter (potassium nitrate), sulfur, and charcoal used as a propellant and explosive",
       "A low-explosive mixture of saltpeter (potassium nitrate), sulfur, and charcoal, used for propulsion, pyrotechnics, and military applications"
      ]
     },
     "fan": [
      {
       "reading": "Pyrotechnic composition with variable ratios",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Consistent historical records of fixed ratios",
       "followup": "Chemical analysis of preserved historical samples"
      },
      {
       "reading": "Originally a medicinal or alchemical elixir (e.g., for immortality) before military use",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Discovery of early gunpowder recipes explicitly for weapons pre-9th century",
       "followup": "Linguistic analysis of early Chinese terms for gunpowder (e.g., 'fire drug')"
      },
      {
       "reading": "Accidental byproduct of metallurgical or saltpeter refining processes",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Documented intentional experimentation with nitrate-sulfur mixtures",
       "followup": "Replication studies of ancient saltpeter production methods"
      },
      {
       "reading": "Variable early composition with lower saltpeter content (e.g., 50%)",
       "weight": 0.2,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "All known early recipes from 11th-12th centuries have at least 60% saltpeter",
       "followup": "Analyze the 'Wujing Zongyao' (1044) recipe and other early documented formulas"
      },
      {
       "reading": "Primarily a military weapon, secondarily a pyrotechnic",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of early non-military uses",
       "followup": "Examine pre-14th century non-military applications"
      },
      {
       "reading": "Early gunpowder included organic binders like honey or lacquer",
       "weight": 0.1,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No historical or chemical evidence of such binders in surviving specimens",
       "followup": "Examine chemical residues from Song dynasty gunpowder artifacts"
      }
     ]
    },
    "where": {
     "leading": "East Asia (origins), spread to Middle East, Europe via Silk Road",
     "agreement": 0.562,
     "sharpness": 0.541,
     "measured_frac": 0.938,
     "perBloc": {
      "CN": [
       "East Asia (origins), spread to Middle East, Europe via Silk Road",
       "China (Tang dynasty, 9th c.), spread via Silk Road to Middle East (13th c.), Europe (13th c.)",
       "Originated in China; spread via Silk Road to Middle East and Europe; global"
      ],
      "US": [
       "Originating in ancient China (c. 9th century CE), spreading via the Silk Road and maritime routes to the Middle East, Europe, and subsequently globally.",
       "Originated in Imperial China, spreading globally via East Asia, Central Asia, the Middle East, and Europe by trade, conquest, and cultural transmission",
       "China, Europe, global spread via trade"
      ],
      "EU": [
       "Originated in China, spread to Middle East, Europe, and globally",
       "Originated in China, spread to Middle East, Europe, and globally via trade and warfare",
       "Originated in China (Tang/Song Dynasties), spread via Silk Road to Islamic world, then Europe, later globalized via colonialism and trade"
      ]
     },
     "fan": [
      {
       "reading": "Single origin point (Tang China)",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Conflicting evidence from 10th c. Islamic texts",
       "followup": "Compare earliest Chinese vs. Arabic recipe chronologies"
      },
      {
       "reading": "First used in China, then transmitted via Silk Road",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "No Silk Road transmission evidence",
       "followup": "Trace gunpowder recipes in medieval trade documents"
      },
      {
       "reading": "Primary diffusion through maritime trade (e.g., Arab dhows) rather than overland routes",
       "weight": 0.4,
       "tag": "estimated",
       "bloc": "EU",
       "falsifier": "Overland transmission evidenced by Mongol-era documents",
       "followup": "Isotopic analysis of saltpeter sources in early gunpowder samples"
      },
      {
       "reading": "Central Asia as early diffusion point",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No 9th-10th c. Central Asian archaeological evidence",
       "followup": "Excavate 9th-10th c. trading posts on Silk Road"
      },
      {
       "reading": "Independent development in multiple regions",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Clear evidence of Chinese transmission",
       "followup": "Compare chemical compositions across regions"
      },
      {
       "reading": "Transmission to Europe via Mongol conquests (13th century) rather than Islamic intermediaries",
       "weight": 0.3,
       "tag": "estimated",
       "bloc": "EU",
       "falsifier": "Earlier European references to gunpowder via Arabic sources (e.g., Roger Bacon)",
       "followup": "Comparison of Mongol-era battlefield accounts with European chronicles"
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
       "9th c. (China) → 10th-13th c. (spread) → 14th c. (military use in Europe)",
       "9th c. China (first documented use), spread 13th c., European refinement 14th-15th c.",
       "c. 850 CE (Tang dynasty) to present"
      ],
      "US": [
       "9th century to present",
       "Known by the Tang Dynasty (China, c. 9th century CE) with significant military application and spread by the 13th-14th centuries, evolving through various formulations to modern high explosives.",
       "Emergence by the 9th century CE in China, with military applications by the 11th century, and significant global spread from the 13th century onwards"
      ],
      "EU": [
       "9th century (China) to present, with key developments in 13th-14th centuries (Europe)",
       "9th century CE (China) to present, with key developments in 13th-15th centuries (Europe)",
       "Invented 9th–10th century CE (Tang/Song transition), refined 11th–13th century (Song Dynasty), transmitted to Europe/Islamic world 13th–14th century, globalized 15th–19th century"
      ]
     },
     "fan": [
      {
       "reading": "c. 400 CE alchemical precursor",
       "weight": 0.9,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No explicit recipe containing all three components",
       "followup": "Examine early alchemical texts for sulfur-saltpeter mixtures"
      },
      {
       "reading": "First recorded in 9th century China, widespread by 13th century",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Earlier records found",
       "followup": "Search for pre-9th century Chinese texts"
      },
      {
       "reading": "Gunpowder's military dominance peaked by 16th century, replaced by high explosives by 19th century",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "EU",
       "falsifier": "Continued use of gunpowder in artillery into 20th century (e.g., WWI)",
       "followup": "Quantitative analysis of military procurement records 16th-19th century"
      },
      {
       "reading": "European development in 13th century without Chinese influence",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Evidence of Chinese transmission",
       "followup": "Analyze European manuscripts for earlier references"
      },
      {
       "reading": "Earliest gunpowder-like mixtures existed in China by 3rd-5th century (e.g., 'fire trees' in alchemical texts)",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "No physical evidence of nitrate-sulfur-charcoal mixtures pre-9th century",
       "followup": "Radiocarbon dating of earliest known gunpowder residues"
      },
      {
       "reading": "First actual explosive use occurred in the 10th century, with earlier 'proto-gunpowder' being purely medicinal",
       "weight": 0.2,
       "tag": "estimated",
       "bloc": "CN",
       "falsifier": "The 1044 'Wujing Zongyao' describes military incendiaries before that date; also indirect evidence from 9th c. alchemical accidents",
       "followup": "Radiocarbon date earliest known gunpowder residue from Dunhuang manuscripts"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "revolutionized warfare",
     "Military revolution (cannons, firearms)",
     "Pyrotechnic displays (festivals, signaling)",
     "Military revolution: cannons in Mongol siege of Xiangyang (1273)",
     "Social disruption: decline of feudal castles, rise of standing armies"
    ],
    "aims_by_bloc": {
     "CN": [
      "Entertainment (fireworks, pyrotechnics)",
      "Elixir of immortality (alchemical purpose)",
      "Fireworks and signaling (practical use)",
      "Longevity elixirs (Tang)"
     ],
     "US": [
      "To achieve conquest and project military dominance through superior destructive and propul",
      "To impress, entertain, and express cultural traditions through spectacular visual and audi",
      "To overcome natural obstacles and extract resources more efficiently (mining and construct",
      "To discover the secrets of nature and achieve transcendence (early alchemical goals)."
     ],
     "EU": [
      "Achieve immortality (alchemical goal)",
      "Develop superior military weapons",
      "Achieve immortality or elixirs of life (alchemical goals)",
      "Develop more powerful weapons for defense and conquest"
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
     960,
     1050,
     1250,
     1279,
     1350,
     1450,
     1650,
     1850
    ]
   }
  },
  {
   "id": "E3",
   "title": "the Diamond Sutra of 868 CE (the specific physical printed scroll from Dunhuang, British Library Or.8210/P.2)",
   "n": 14,
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
     "leading": "Buddhist monks and scholars",
     "agreement": 0.5,
     "sharpness": 0.479,
     "measured_frac": 0.929,
     "perBloc": {
      "CN": [
       "Chinese woodblock printers (Chang'an)",
       "Buddhist monk Huichang (printer), Dunhuang monastery, Silk Road monks",
       "Wang Jie (commissioner), unknown block carver, Kumarajiva (translator), Aurel Stein (discoverer), British Library (custodian)"
      ],
      "US": [
       "Buddhist monks and scholars",
       "Buddhist scribes, translators, and patrons involved in its production and preservation at Dunhuang",
       "sacred Buddhist monks and translators"
      ],
      "EU": [
       "Buddhist monks and lay scribes in Dunhuang, Tang dynasty officials, Central Asian traders, British Library curators",
       "Buddhist monks of Dunhuang, British Library curators, scholars",
       "Buddhist monks of Dunhuang, British Library curators"
      ]
     },
     "fan": [
      {
       "reading": "Korean Buddhist monks",
       "weight": 0.7,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Korean woodblock prints dated later (9th c. post-868)",
       "followup": "Compare block-cutting techniques to Korean extant examples"
      },
      {
       "reading": "Local Dunhuang Buddhist monk (no name recorded)",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Documented printer's signature on scroll",
       "followup": "Examine ink residue for named calligrapher's mark"
      },
      {
       "reading": "Monks of the Jingtu Temple",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Discovery of secular workshop guild marks on the block",
       "followup": "Comparative analysis of ink composition against known secular vs monastic inks"
      },
      {
       "reading": "Dunhuang monks",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Lack of other records from Dunhuang monks",
       "followup": "Examine other manuscripts for monk attribution"
      },
      {
       "reading": "Chinese scholars in general",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Specific attribution to a single school or sect",
       "followup": "Investigate citations or usage by specific schools"
      },
      {
       "reading": "State-sponsored printing bureau (Xi'an)",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No imperial mint records from 868 CE",
       "followup": "Search state archives for 9th c. printing permits"
      }
     ]
    },
    "what": {
     "leading": "printed Buddhist scripture",
     "agreement": 0.786,
     "sharpness": 0.786,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "Woodblock-printed silk Buddhist scripture scroll",
       "Woodblock-printed Buddhist sutra on paper",
       "Woodblock-printed scroll of the Diamond Sutra, ink on paper, dated 868 CE, approximately 5.5 m long"
      ],
      "US": [
       "printed Buddhist scripture",
       "The earliest dated, complete printed Buddhist codex, comprising the Vajracchedikā Prajñāpāramitā Sūtra, produced on paper using woodblock printing for religious devotion and propagation.",
       "printed scroll of Buddhist scripture"
      ],
      "EU": [
       "Woodblock-printed Buddhist scripture (Mahayana sutra) on paper scroll, earliest dated complete printed book",
       "Woodblock-printed Buddhist scripture on silk",
       "Woodblock-printed Buddhist sutra scroll"
      ]
     },
     "fan": [
      {
       "reading": "Multiple-woodblock inked print",
       "weight": 0.7,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Microscopic scan shows single-block edges",
       "followup": "3D reconstruction of ink layers"
      },
      {
       "reading": "Artifact of religious doctrine",
       "weight": 0.6,
       "tag": "measured",
       "bloc": "US",
       "falsifier": "Documentation of non-religious uses",
       "followup": "Search for mentions of secular use in contemporary texts"
      },
      {
       "reading": "Material cultural heritage",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Lack of archaeological contexts linking to culture",
       "followup": "Explore wider contexts of artefacts found in Dunhuang"
      },
      {
       "reading": "Stenciled manuscript",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Distinct printed grain pattern in paper",
       "followup": "Compare to 8th c. stenciled fragments from Turfan"
      },
      {
       "reading": "early form of woodblock printing",
       "weight": 0.2,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "discovery of an earlier printing method",
       "followup": "comparison with other early printed materials"
      },
      {
       "reading": "Ritual object with talismanic function beyond textual content",
       "weight": 0.15,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Absence of ritual wear patterns or votive inscriptions",
       "followup": "Use-wear analysis and comparison with other Dunhuang ritual scrolls"
      }
     ]
    },
    "where": {
     "leading": "Origin: Chang'an (Tang China); Spread: Dunhuang (Gansu) → British Library (London)",
     "agreement": 0.5,
     "sharpness": 0.479,
     "measured_frac": 0.929,
     "perBloc": {
      "CN": [
       "Origin: Chang'an (Tang China); Spread: Dunhuang (Gansu) → British Library (London)",
       "Dunhuang (Gansu, China), spread to Dunhuang monastery, British Library (London)",
       "Produced in Dunhuang, discovered in Mogao Cave 17, now at British Library (London)"
      ],
      "US": [
       "Originated and preserved within the Mogao Caves Library Cave complex near Dunhuang, Gansu Province, China.",
       "Dunhuang, China; later British Library",
       "Dunhuang, later British Library"
      ],
      "EU": [
       "Dunhuang, Mogao Caves (origin); British Library (current)",
       "Dunhuang (origin), British Library (current)",
       "Originated in Dunhuang (Gansu, China), stored in Mogao Caves, now British Library (London)"
      ]
     },
     "fan": [
      {
       "reading": "Silk Road merchants",
       "weight": 0.6,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No merchant records or trade routes documented for this item",
       "followup": "Examine Dunhuang curation logs for acquisition context"
      },
      {
       "reading": "Primarily in China",
       "weight": 0.55,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Discovery of similar artifacts in other regions",
       "followup": "Conduct comparative studies across sites"
      },
      {
       "reading": "Dunhuang origin → Dunhuang monastery collection",
       "weight": 0.5,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Dunhuang caves inscription dates",
       "followup": "Correlate excavation dates from Cave 17"
      },
      {
       "reading": "Dunhuang → Samarkand (Sogdian trade) → London",
       "weight": 0.5,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No Arabic trade records mentioning it",
       "followup": "Query Sogdian merchant archives in Central Asian libraries"
      },
      {
       "reading": "Global dissemination through trade",
       "weight": 0.45,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence of its absence in historical trade records",
       "followup": "Analyze trade routes to determine spread"
      },
      {
       "reading": "Buddhist monastic centers in Xinjiang",
       "weight": 0.4,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "No Dunhuang monastery records link to this specific scroll",
       "followup": "Cross-reference with Dunhuang cave inventory records"
      }
     ]
    },
    "when": {
     "leading": "868 CE (production) → Dunhuang use (868-1907) → British Library (1907-present)",
     "agreement": 0.143,
     "sharpness": 0.143,
     "measured_frac": 1.0,
     "perBloc": {
      "CN": [
       "868 CE (production) → Dunhuang use (868-1907) → British Library (1907-present)",
       "868 CE (production), 19th c. (discovery), 1900s (acquisition by British Library)",
       "Created 868 CE (colophon date), discovered 1900 CE, acquired by Stein 1907 CE, entered British Museum 1914 CE, transferred to British Library 1973 CE"
      ],
      "US": [
       "Created in 868 CE, preserved within the Dunhuang library cave, and discovered in the early 20th century.",
       "868 CE; first printing and dissemination to modern times",
       "Printed circa 868 CE; influential over centuries"
      ],
      "EU": [
       "868 CE (printed); 1907 (discovered by Aurel Stein); 20th-21st century (digitized)",
       "868 CE (printed), 1907 (discovered), 20th century (studied)",
       "Printed 868 CE (colophon date), created 5th–10th century CE (scroll's paper/ink), stored until 20th century, now archived"
      ]
     },
     "fan": [
      {
       "reading": "Active in Dunhuang until 984 CE",
       "weight": 0.8,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Dunhuang cave sealed 1007 CE; no later usage evidence",
       "followup": "Check cave stratigraphy for associated artifacts"
      },
      {
       "reading": "868 CE (fixed by inscription)",
       "weight": 0.8,
       "tag": "measured",
       "bloc": "CN",
       "falsifier": "Carbon-14 test of paper dated 700-1000 CE",
       "followup": "Re-test paper fibers with AMS dating"
      },
      {
       "reading": "Continued impact until the modern era",
       "weight": 0.7,
       "tag": "estimated",
       "bloc": "US",
       "falsifier": "Lack of later adaptations or copies",
       "followup": "Inspect manuscript trails post-868 CE"
      },
      {
       "reading": "Impact primarily limited to Tang Dynasty",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "US",
       "falsifier": "Evidence of use beyond Tang era",
       "followup": "Investigate references in post-Tang literature"
      },
      {
       "reading": "Woodblock carved decades earlier and reused in 868 CE",
       "weight": 0.3,
       "tag": "conjectured",
       "bloc": "EU",
       "falsifier": "Uniform wear on woodblock characters across the scroll",
       "followup": "3D scanning of character impressions for wear patterns"
      },
      {
       "reading": "Produced before 850 CE",
       "weight": 0.2,
       "tag": "conjectured",
       "bloc": "CN",
       "falsifier": "Colophon explicitly states 868 CE",
       "followup": "Verify inscription chronology against Tang dynasty dating"
      }
     ]
    }
   },
   "why": {
    "delivered": [
     "Proof of mass woodblock printing technology",
     "Preservation of Buddhist texts across eras",
     "Proven existence of woodblock printing in China 868 CE",
     "Established itself as the world's earliest dated, complete printed book, revolutionizing t",
     "Preserved a significant Buddhist scripture and provided invaluable data on Tang Dynasty pr"
    ],
    "aims_by_bloc": {
     "CN": [
      "Mass religious distribution to monasteries",
      "Scholarly study of Buddhist doctrine",
      "Monastic study (Buddhist doctrine dissemination)",
      "Royal diplomacy (gift to Tibetans)"
     ],
     "US": [
      "To serve as a tool for individual spiritual enlightenment and merit accumulation through r",
      "To be a devotional object, an act of religious offering, or a repository of Buddhist teach",
      "To serve as a demonstration of the patron's or printer's piety and resources.",
      "to propagate the essence of Buddhist philosophy"
     ],
     "EU": [
      "Spread Buddhist teachings",
      "Serve as a ceremonial object",
      "Spiritual enlightenment of readers",
      "Political or cultural influence"
     ]
    },
    "complementarity": 0.97
   },
   "when_span": {
    "start": 868,
    "end": 2050,
    "markers": [
     868,
     950,
     1000,
     1850,
     1900,
     1907,
     1914,
     1950,
     1973,
     2050
    ]
   }
  }
 ],
 "blocs": {
  "CN": "#e0564b",
  "US": "#4b8fe0",
  "EU": "#56c08a"
 }
};
