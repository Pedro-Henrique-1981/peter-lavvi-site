/**
 * PORTAL MAP ENGINE — Leaflet 1.9.4 GIS Radar Integration
 * Pedro Soares • Lavvi Private Wealth
 *
 * Exposes:
 *  - window.renderMapFilters(filterKey)
 *  - window.openPropertyModal(itemOrId, contextType)
 *  - window.applyPortalMapFilter(filterKey, btn)
 *  - window.closePropertyModal()
 */

(function () {
  'use strict';

  // 12 Market Competitor Benchmarks (Cyrela, Trisul, Mitre, EZTEC, JFL Living, etc.)
  const MARKET_COMPETITORS = [
    {
      "id": "parque_global",
      "nome": "Parque Global Residences",
      "incorporadora": "Benx / Trisul",
      "bairro": "Santo Amaro / Marginal",
      "endereco": "Av. Marginal Pinheiros, 14500",
      "ll": [-23.6262, -46.7118],
      "m2": "142 a 384 m²",
      "units": "3 a 4 Suítes • 2 a 4 Vagas",
      "preco_m2": "R$ 22.000 a R$ 28.000/m²",
      "preco_partida": "R$ 3.200.000",
      "status": "Em Obras",
      "entrega": "Fases 2025-2027",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/20b362e7-f04b-4a11-9387-137c3483da4f_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "Jardim da Hípica oferece bairro estritamente residencial (Alto da Boa Vista), 39.553 m² de terreno com praça de 10.000 m² e assessoria Body Care inclusa no condomínio, sem o fluxo comercial da Marginal.",
      "diferenciais": [
        "Terreno massivo com shopping e universidade vizinhos",
        "Torres de altíssimo padrão com vista para a Marginal Pinheiros",
        "Complexo multiúso de grande circulação pública"
      ]
    },
    {
      "id": "parque_da_cidade",
      "nome": "Parque da Cidade Residences",
      "incorporadora": "EZTEC",
      "bairro": "Chácara Santo Antônio",
      "endereco": "Av. das Nações Unidas, 14401",
      "ll": [-23.6231, -46.7032],
      "m2": "135 a 258 m²",
      "units": "3 e 4 Suítes • 2 a 3 Vagas",
      "preco_m2": "R$ 21.000 a R$ 26.000/m²",
      "preco_partida": "R$ 2.900.000",
      "status": "Pronto para Morar",
      "entrega": "Entregue",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/735c0211-1a3b-4861-ab8a-8285514f165e_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "Jardim da Hípica possui fração ideal superior em terreno 100% privativo de 40.000 m², 2 quadras de tênis oficiais e raia de 60m, sem divisão de área com torres de escritórios corporativos.",
      "diferenciais": [
        "Integração ao shopping Parque da Cidade e hotel Four Seasons",
        "Parque linear corporativo interno",
        "Certificação LEED Gold e sustentabilidade energética"
      ]
    },
    {
      "id": "on_the_sky",
      "nome": "On The Sky Cyrela",
      "incorporadora": "Cyrela",
      "bairro": "Brooklin / Chucri Zaidan",
      "endereco": "Rua Alexandre Dumas, 1711",
      "ll": [-23.6288, -46.7022],
      "m2": "28 a 150 m²",
      "units": "Studios, 1 a 3 Suítes",
      "preco_m2": "R$ 18.500 a R$ 24.000/m²",
      "preco_partida": "R$ 550.000",
      "status": "Em Obras",
      "entrega": "Dezembro/2026",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/6df6c41b-a489-49aa-971c-3093282b5454_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "Jardim da Hípica privilegia o refúgio familiar com lazer de resort em 40.000 m² no Alto da Boa Vista, contra o perfil corporativo/investidor de eixo viário do Brooklin.",
      "diferenciais": [
        "Rooftop icônico com piscina suspensa nas alturas",
        "Studios de investimento e residências familiares em torre única",
        "Ao lado dos polos corporativos da Berrini e Chucri Zaidan"
      ]
    },
    {
      "id": "haus_mitre_chacara",
      "nome": "Haus Mitre Chácara Santo Antônio",
      "incorporadora": "Mitre Realty",
      "bairro": "Chácara Santo Antônio",
      "endereco": "Rua Fernandes Moreira, 1100",
      "ll": [-23.6338, -46.6995],
      "m2": "65 a 110 m²",
      "units": "2 e 3 Dorms (1 a 3 Suítes)",
      "preco_m2": "R$ 15.500 a R$ 18.200/m²",
      "preco_partida": "R$ 1.050.000",
      "status": "Em Obras",
      "entrega": "Outubro/2026",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/20b362e7-f04b-4a11-9387-137c3483da4f_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "Terreno convencional compacto de torre isolada vs. o complexo de 40.000 m² do Jardim da Hípica, que entrega 2 quadras de tênis oficiais (18x36m), 2 quadras de beach tennis e raia de 60m.",
      "diferenciais": [
        "Lazer assinado na cobertura com piscina de borda infinita",
        "Plantas inteligentes para famílias jovens",
        "Proximidade aos colégios Elvira Brandão e Rudolf Steiner"
      ]
    },
    {
      "id": "valente_paraiso",
      "nome": "Valente Paraíso",
      "incorporadora": "Trisul",
      "bairro": "Paraíso",
      "endereco": "Rua Valente de Almeida, 85",
      "ll": [-23.5742, -46.648],
      "m2": "120 a 165 m²",
      "units": "3 e 4 Dorms (2 a 3 Suítes)",
      "preco_m2": "R$ 22.000 a R$ 27.500/m²",
      "preco_partida": "R$ 2.640.000",
      "status": "Em Obras",
      "entrega": "Março/2027",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/fa66f48a-6663-4702-b2f7-f027e8d7a188_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "T.O.M. Paraíso oferece terreno incomparável de 5.600 m² e minuta de convenção em cartório com liberação formal para Airbnb no R2V, garantindo liquidez contra assembleias restritivas.",
      "diferenciais": [
        "Localização privilegiada a passos do Parque Ibirapuera",
        "Acabamentos nobres em mármore importado nas áreas comuns",
        "Lazer de clube completo com piscina aquecida"
      ]
    },
    {
      "id": "cyrela_for_you_paraiso",
      "nome": "Cyrela For You Paraíso",
      "incorporadora": "Cyrela",
      "bairro": "Paraíso",
      "endereco": "Rua Tomás Carvalhal, 300",
      "ll": [-23.5765, -46.6455],
      "m2": "25 a 45 m²",
      "units": "Studios e 1 Dorm",
      "preco_m2": "R$ 20.000 a R$ 24.000/m²",
      "preco_partida": "R$ 510.000",
      "status": "Em Obras",
      "entrega": "Novembro/2026",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/6df6c41b-a489-49aa-971c-3093282b5454_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "T.O.M. Paraíso conjuga studios com torre residencial de grande escala e terreno de 5.600 m² a 240m do Metrô Paraíso, permitindo fluxo 47/53 atrativo para investidores.",
      "diferenciais": [
        "Conceito boutique moderno para locação urbana",
        "Coworking completo e lavanderia coletiva OMO",
        "A 300 metros da Estação Paraíso do Metrô"
      ]
    },
    {
      "id": "oscar_paraiso",
      "nome": "Oscar Paraíso",
      "incorporadora": "Trisul",
      "bairro": "Paraíso",
      "endereco": "Rua Oscar Porto, 550",
      "ll": [-23.5755, -46.644],
      "m2": "140 a 210 m²",
      "units": "3 e 4 Suítes • 2 a 3 Vagas",
      "preco_m2": "R$ 23.000 a R$ 29.000/m²",
      "preco_partida": "R$ 3.220.000",
      "status": "Em Obras",
      "entrega": "Agosto/2027",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/20b362e7-f04b-4a11-9387-137c3483da4f_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "Le Six Paraíso oferece concierge CBRE e assessoria Body Care inclusos por 3 anos, além de arquitetura com vedações convencionais maciças anti-ruído.",
      "diferenciais": [
        "Arquitetura contemporânea de alto padrão",
        "Áreas comuns assinadas com mobiliário de design nacional",
        "Quadra de tênis coberta no condomínio"
      ]
    },
    {
      "id": "haus_mitre_paraiso",
      "nome": "Haus Mitre Paraíso",
      "incorporadora": "Mitre Realty",
      "bairro": "Paraíso",
      "endereco": "Rua Abílio Soares, 450",
      "ll": [-23.573, -46.6495],
      "m2": "60 a 125 m²",
      "units": "2 e 3 Dorms (1 a 3 Suítes)",
      "preco_m2": "R$ 18.000 a R$ 22.500/m²",
      "preco_partida": "R$ 1.100.000",
      "status": "Em Obras",
      "entrega": "Junho/2026",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/fa66f48a-6663-4702-b2f7-f027e8d7a188_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "T.O.M. Paraíso possui 5.600 m² de terreno com áreas de lazer amplas e design Triplex Arquitetura, a 350m do HCor e 240m do Metrô Paraíso.",
      "diferenciais": [
        "Lazer elevado com vista panorâmica para o Parque Ibirapuera",
        "Pontos para recarga de carro elétrico na garagem",
        "Fitness com equipamentos profissionais Technogym"
      ]
    },
    {
      "id": "cyrela_heritage",
      "nome": "Heritage by Pininfarina",
      "incorporadora": "Cyrela",
      "bairro": "Itaim Bibi / Vila Nova Conceição",
      "endereco": "Rua Leopoldo Couto de Magalhães Jr, 1200",
      "ll": [-23.5855, -46.678],
      "m2": "570 m²",
      "units": "4 Suítes • 6 a 8 Vagas",
      "preco_m2": "R$ 45.000 a R$ 60.000/m²",
      "preco_partida": "R$ 25.000.000",
      "status": "Pronto para Morar",
      "entrega": "Entregue",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/735c0211-1a3b-4861-ab8a-8285514f165e_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "Saffire by Elie Saab em Moema Pássaros entrega grife de alta costura internacional comparável com terreno de 7.600 m² e ticket de entrada com liquidez patrimonial consideravelmente superior.",
      "diferenciais": [
        "Design aerodinâmico icônico assinado pelo estúdio Pininfarina",
        "1 unidade por andar com 570 m² e pé-direito duplo",
        "Garagem de colecionador e spa privativo"
      ]
    },
    {
      "id": "jfl_vhouse",
      "nome": "VHouse / VO699",
      "incorporadora": "JFL Living",
      "bairro": "Faria Lima / Moema",
      "endereco": "Av. Brigadeiro Faria Lima, 4300",
      "ll": [-23.571, -46.691],
      "m2": "38 a 92 m²",
      "units": "Studios e 1 a 2 Dorms",
      "preco_m2": "Sob Consulta (Locação de Renda)",
      "preco_partida": "Locação Gerida",
      "status": "Pronto para Morar",
      "entrega": "Operação Ativa",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/6df6c41b-a489-49aa-971c-3093282b5454_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "O modelo JFL Living opera com locação restrita e gestão centralizada da operadora. A Lavvi oferece imóveis 100% escriturados para o investidor com liberdade total de uso, revenda e rendimento líquido sem taxa de carregamento de fundo.",
      "diferenciais": [
        "Operação profissional de short e long stay corporativo",
        "Serviço de hotelaria 5 estrelas e concierge bilíngue",
        "Mobiliário e enxoval completos de alto padrão"
      ]
    },
    {
      "id": "haus_mitre_brooklin",
      "nome": "Haus Mitre Brooklin",
      "incorporadora": "Mitre Realty",
      "bairro": "Brooklin",
      "endereco": "Av. Nova Independência, 890",
      "ll": [-23.612, -46.685],
      "m2": "28 a 85 m²",
      "units": "Studios e 2 Dorms (1 Suíte)",
      "preco_m2": "R$ 16.000 a R$ 20.000/m²",
      "preco_partida": "R$ 490.000",
      "status": "Em Obras",
      "entrega": "Julho/2026",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/20b362e7-f04b-4a11-9387-137c3483da4f_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "Petra by Boca do Lobo no Brooklin (Av. Roque Petroni Jr, 305) entrega 5.701 m² de terreno, design de mobiliário assinado e plantas de 162 a 199 m² com qualidade construtiva Cyrela.",
      "diferenciais": [
        "A 600m da estação Campo Belo da Linha 5-Lilás",
        "Lazer nas alturas com vista panorâmica para a Ponte Estaiada",
        "Fachada com painéis metálicos e iluminação cênica"
      ]
    },
    {
      "id": "raizes_chacara_sto_antonio",
      "nome": "Raízes Chácara Santo Antônio",
      "incorporadora": "Mitre Realty",
      "bairro": "Chácara Santo Antônio",
      "endereco": "Rua Américo Brasiliense, 2100",
      "ll": [-23.631, -46.702],
      "m2": "65 a 110 m²",
      "units": "2 e 3 Dorms (1 a 3 Suítes)",
      "preco_m2": "R$ 15.000 a R$ 17.800/m²",
      "preco_partida": "R$ 990.000",
      "status": "Em Obras",
      "entrega": "Dezembro/2026",
      "hero_image": "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/735c0211-1a3b-4861-ab8a-8285514f165e_1_perspectiva_ilustrada_da_fachada.webp",
      "assimetria_lavvi": "Jardim da Hípica supera em escala urbana com 40.000 m² de terreno, 2 quadras de tênis oficiais (18x36m), 2 quadras de beach tennis, raia de 60m e assessoria esportiva Body Care inclusa no condomínio.",
      "diferenciais": [
        "Lazer de clube completo para a família",
        "A 400m da estação Borba Gato do Metrô",
        "Varanda gourmet integrada ao living"
      ]
    }
  ];

  // 8 Anchor Clusters Fallback (Zero-CORS / Local File Resilience)
  const ANCHOR_CLUSTERS_FALLBACK = {
    categories: {
      "emporios": { "label": "St. Marche & Empórios Nobres", "icon": "🛒", "color": "#10B981" },
      "pizzarias": { "label": "Pizzas & Forno a Lenha (Bráz)", "icon": "🍕", "color": "#F59E0B" },
      "adegas": { "label": "Wine Houses & Adegas", "icon": "🍷", "color": "#8B5CF6" },
      "clubes": { "label": "Tênis, Padel & Squash", "icon": "🎾", "color": "#3B82F6" },
      "wellness": { "label": "Piscinas & Raia Olímpica", "icon": "🏊", "color": "#06B6D4" },
      "gastronomia": { "label": "Alta Gastronomia", "icon": "🍴", "color": "#EC4899" },
      "escolas": { "label": "Colégios Bilíngues & Internacionais", "icon": "🎓", "color": "#6366F1" },
      "parques": { "label": "Parques & Bosques Preservados", "icon": "🌳", "color": "#10B981" },
      "saude": { "label": "Hospitais & Maternidades de Elite", "icon": "🏥", "color": "#EF4444" },
      "iguatemi": { "label": "Índice Iguatemi (Marcas de Grife)", "icon": "💎", "color": "#D4AF37" },
      "michelin": { "label": "Guia Michelin & 50 Best", "icon": "⭐", "color": "#B91C1C" }
    },
    projects: {
      "hipica": {
        "nome": "Jardim da Hípica",
        "bairro": "Alto da Boa Vista",
        "endereco": "Rua Antônio Bandeira, 305",
        "lat": -23.6402,
        "lon": -46.7025,
        "lifestyle_score": 96,
        "destaque_condominio": "Empreendimento com terreno de ~40.000 m² (39.553 m²) em frente ao Clube Hípico de Santo Amaro (CHSA).",
        "specs_oficiais": {
          "terreno": "39.553 m² (~40.000 m²) + Praça de 10.000 m²",
          "tipologias": "Residences 84 m² a 276 m² + Studios 21 m² a 57 m²",
          "preco_partida": "R$ 1.190.000",
          "preco_m2": "R$ 13.890 a R$ 17.500 / m²",
          "fluxo": "35% obra + 65% chaves",
          "lazer_destaque": "02 Quadras de Tênis Oficiais (18x36m) + 02 Beach Tennis + Piscina raia 60m + 04 Private Houses",
          "gestao_servicos": "CBRE + Body Care inclusa no condomínio"
        },
        "pois": []
      },
      "moema": {
        "nome": "Villa Moema & Saffire by Elie Saab",
        "bairro": "Moema Pássaros",
        "endereco": "Rua Gaivota, 550",
        "lat": -23.6025,
        "lon": -46.6625,
        "lifestyle_score": 98,
        "destaque_condominio": "Quadrilátero nobre de Moema Pássaros, a poucos metros do Parque Ibirapuera.",
        "specs_oficiais": {
          "terreno": "7.600 m² de terreno nobre",
          "tipologias": "360 m² e 493 m² (coberturas até 868 m²)",
          "preco_partida": "R$ 7.900.000",
          "lazer_destaque": "Interiores assinados por Elie Saab e Versace Home"
        },
        "pois": []
      },
      "paraiso": {
        "nome": "T.O.M. Paraíso & Le Six",
        "bairro": "Paraíso",
        "endereco": "Rua Tomás Carvalhal, 92",
        "lat": -23.578,
        "lon": -46.648,
        "lifestyle_score": 97,
        "destaque_condominio": "A 240m do Metrô Paraíso e 350m do HCor, com liberação de Airbnb em cartório no R2V.",
        "specs_oficiais": {
          "terreno": "5.600 m² no Paraíso",
          "tipologias": "Studios 24 a 45 m² + 2 a 4 Dorms (65 a 264 m²)",
          "preco_partida": "R$ 490.000",
          "lazer_destaque": "Triplex Arquitetura e lazer de resort completo"
        },
        "pois": []
      },
      "brooklin": {
        "nome": "Wonder Brooklin & Petra",
        "bairro": "Brooklin",
        "endereco": "Av. Roque Petroni Júnior, 305",
        "lat": -23.6185,
        "lon": -46.689,
        "lifestyle_score": 95,
        "destaque_condominio": "A 350m do Metrô Brooklin com assinatura exclusiva Boca do Lobo.",
        "specs_oficiais": {
          "terreno": "5.701 m² no Brooklin",
          "tipologias": "162 m² e 199 m² (3 e 4 suítes)",
          "preco_partida": "R$ 2.450.000",
          "lazer_destaque": "Mobiliário internacional assinado e lazer resort"
        },
        "pois": []
      },
      "well_perdizes": {
        "nome": "Well Perdizes & Novvo Santa Marina",
        "bairro": "Perdizes",
        "endereco": "Rua João Ramalho, 1150",
        "lat": -23.535,
        "lon": -46.678,
        "lifestyle_score": 94,
        "destaque_condominio": "A passos da PUC-SP com alta liquidez de locação.",
        "specs_oficiais": {
          "terreno": "1.252 m² em Perdizes",
          "tipologias": "Studios 21 m² a 38 m² e 2 Dorms",
          "preco_partida": "R$ 380.000"
        },
        "pois": []
      },
      "klabin": {
        "nome": "Soleil & Galleria Klabin",
        "bairro": "Chácara Klabin / Vila Mariana",
        "endereco": "Rua Vergueiro, 3100",
        "lat": -23.5895,
        "lon": -46.632,
        "lifestyle_score": 95,
        "destaque_condominio": "Interiores por Boca do Lobo e conveniência de metrô duplo (Linha Verde/Lilás).",
        "specs_oficiais": {
          "tipologias": "Residences 246 m²",
          "preco_partida": "R$ 3.800.000"
        },
        "pois": []
      },
      "analia_franco": {
        "nome": "Novvo Anália Franco & High Wonder",
        "bairro": "Jardim Anália Franco",
        "endereco": "Av. Regente Feijó, 1200",
        "lat": -23.558,
        "lon": -46.5615,
        "lifestyle_score": 93,
        "destaque_condominio": "Eixo Shopping Anália Franco com alta valorização na Zona Leste.",
        "specs_oficiais": {
          "tipologias": "Studios e 1 e 2 Dorms",
          "preco_partida": "R$ 290.000"
        },
        "pois": []
      },
      "marajoara": {
        "nome": "Novvo Marajoara & Alive",
        "bairro": "Jardim Marajoara",
        "endereco": "Av. Washington Luís, 3800",
        "lat": -23.665,
        "lon": -46.685,
        "lifestyle_score": 92,
        "destaque_condominio": "Smart living junto a colégios tradicionais e vias de acesso na Zona Sul.",
        "specs_oficiais": {
          "tipologias": "Studios e 1 e 2 Dorms",
          "preco_partida": "R$ 270.000"
        },
        "pois": []
      }
    }
  };

  // State Variables
  let portalMapInstance = null;
  let portalMarkersLayer = null;
  let portalCirclesLayer = null;
  let currentPortalFilter = 'todos';
  let cachedRadarData = null;
  let previousActiveElement = null;

  // Custom Icon Definitions
  let goldIcon = null;
  let novvoIcon = null;
  let historicoIcon = null;
  let compIcon = null;

  function initIcons() {
    if (typeof L === 'undefined') return;

    goldIcon = L.divIcon({
      className: 'gpin',
      html: `
        <div class="gpin-radar"></div>
        <svg width="24" height="30" viewBox="0 0 24 32" fill="none" style="filter: drop-shadow(0 2px 5px rgba(0,0,0,0.4)); position: relative; z-index: 2;">
          <path d="M12 0C5.37 0 0 5.37 0 12C0 21 12 32 12 32C12 32 24 21 24 12C24 5.37 18.63 0 12 0Z" fill="#182842"/>
          <path d="M12 2C6.48 2 2 6.48 2 12C2 19.5 12 29.5 12 29.5C12 29.5 22 19.5 22 12C22 6.48 17.52 2 12 2Z" fill="#957b2b"/>
          <circle cx="12" cy="12" r="5" fill="#F3DC8A"/>
        </svg>
      `,
      iconSize: [24, 30],
      iconAnchor: [12, 30],
      popupAnchor: [0, -28]
    });

    novvoIcon = L.divIcon({
      className: 'gpin',
      html: `
        <div class="gpin-radar-novvo"></div>
        <svg width="24" height="30" viewBox="0 0 24 32" fill="none" style="filter: drop-shadow(0 2px 5px rgba(0,0,0,0.4)); position: relative; z-index: 2;">
          <path d="M12 0C5.37 0 0 5.37 0 12C0 21 12 32 12 32C12 32 24 21 24 12C24 5.37 18.63 0 12 0Z" fill="#22343E"/>
          <path d="M12 2C6.48 2 2 6.48 2 12C2 19.5 12 29.5 12 29.5C12 29.5 22 19.5 22 12C22 6.48 17.52 2 12 2Z" fill="#A06F71"/>
          <circle cx="12" cy="12" r="5" fill="#FCE7F3"/>
        </svg>
      `,
      iconSize: [24, 30],
      iconAnchor: [12, 30],
      popupAnchor: [0, -28]
    });

    historicoIcon = L.divIcon({
      className: 'gpin',
      html: `
        <div class="gpin-radar-historico"></div>
        <svg width="26" height="32" viewBox="0 0 24 32" fill="none" style="filter: drop-shadow(0 2px 5px rgba(0,0,0,0.35)); position: relative; z-index: 2;">
          <path d="M12 0C5.37 0 0 5.37 0 12C0 21 12 32 12 32C12 32 24 21 24 12C24 5.37 18.63 0 12 0Z" fill="#334155"/>
          <path d="M12 2C6.48 2 2 6.48 2 12C2 19.5 12 29.5 12 29.5C12 29.5 22 19.5 22 12C22 6.48 17.52 2 12 2Z" fill="#D4AF37"/>
          <circle cx="12" cy="12" r="5" fill="#FFFFFF"/>
        </svg>
      `,
      iconSize: [26, 32],
      iconAnchor: [13, 32],
      popupAnchor: [0, -30]
    });

    compIcon = L.divIcon({
      className: 'gpin',
      html: `
        <div class="gpin-radar-comp"></div>
        <svg width="24" height="30" viewBox="0 0 24 32" fill="none" style="filter: drop-shadow(0 2px 5px rgba(0,0,0,0.35)); position: relative; z-index: 2;">
          <path d="M12 0C5.37 0 0 5.37 0 12C0 21 12 32 12 32C12 32 24 21 24 12C24 5.37 18.63 0 12 0Z" fill="#1E293B"/>
          <path d="M12 2C6.48 2 2 6.48 2 12C2 19.5 12 29.5 12 29.5C12 29.5 22 19.5 22 12C22 6.48 17.52 2 12 2Z" fill="#94A3B8"/>
          <circle cx="12" cy="12" r="5" fill="#E2E8F0"/>
        </svg>
      `,
      iconSize: [24, 30],
      iconAnchor: [12, 30],
      popupAnchor: [0, -28]
    });
  }

  function getProjectsList() {
    if (window.allProjects && Array.isArray(window.allProjects) && window.allProjects.length > 0) {
      return window.allProjects;
    }
    return [];
  }

  // Asynchronous POI fetch with cluster fallback
  function loadPoiRadarData(callback) {
    if (cachedRadarData) {
      if (typeof callback === 'function') callback(cachedRadarData);
      return;
    }

    if (typeof fetch === 'function') {
      fetch('poi_radar_data.json')
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        })
        .then(function (data) {
          cachedRadarData = data;
          if (typeof callback === 'function') callback(cachedRadarData);
        })
        .catch(function () {
          cachedRadarData = ANCHOR_CLUSTERS_FALLBACK;
          if (typeof callback === 'function') callback(cachedRadarData);
        });
    } else {
      cachedRadarData = ANCHOR_CLUSTERS_FALLBACK;
      if (typeof callback === 'function') callback(cachedRadarData);
    }
  }

  // Pre-fetch POI data during idle to guarantee smooth UX
  if (typeof window !== 'undefined') {
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(function () { loadPoiRadarData(); });
    } else {
      setTimeout(function () { loadPoiRadarData(); }, 2000);
    }
  }

  // Initialize Embedded Leaflet Map on #portal-map
  function initPortalMap() {
    const mapContainer = document.getElementById('portal-map');
    if (!mapContainer || portalMapInstance) return;
    if (typeof L === 'undefined') return;

    initIcons();

    portalMapInstance = L.map('portal-map', {
      center: [-23.585, -46.665],
      zoom: 12,
      minZoom: 10,
      maxZoom: 17,
      zoomControl: true,
      scrollWheelZoom: false // Anti-scroll-trap: disabled by default
    });

    // Esri World Light Gray Base & Labels
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Tiles &copy; Esri',
      maxZoom: 16
    }).addTo(portalMapInstance);

    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Labels &copy; Esri',
      maxZoom: 16
    }).addTo(portalMapInstance);

    portalMarkersLayer = L.layerGroup().addTo(portalMapInstance);
    portalCirclesLayer = L.layerGroup().addTo(portalMapInstance);

    // Anti-Scroll-Trap Event Handlers
    const hintEl = document.getElementById('portal-scroll-hint');

    portalMapInstance.on('focus click', function () {
      portalMapInstance.scrollWheelZoom.enable();
      if (hintEl) hintEl.style.opacity = '0';
    });

    mapContainer.addEventListener('mouseleave', function () {
      if (portalMapInstance) {
        portalMapInstance.scrollWheelZoom.disable();
      }
      if (hintEl) hintEl.style.opacity = '1';
    });

    // Render initial filter
    window.renderMapFilters('todos');
  }

  // Triggered by Segmented Filter Buttons
  window.applyPortalMapFilter = function (filterKey, btn) {
    currentPortalFilter = filterKey;

    document.querySelectorAll('.mapa-section .ll-filter-pill').forEach(function (pill) {
      pill.classList.remove('active');
      pill.setAttribute('aria-selected', 'false');
    });

    if (btn) {
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
    } else {
      const targetBtn = document.getElementById('portal-filter-' + filterKey);
      if (targetBtn) {
        targetBtn.classList.add('active');
        targetBtn.setAttribute('aria-selected', 'true');
      }
    }

    window.renderMapFilters(filterKey);
  };

  // Public Interface Contract 1: renderMapFilters(filterKey)
  window.renderMapFilters = function (filterKey) {
    currentPortalFilter = filterKey || 'todos';

    if (!portalMapInstance || !portalMarkersLayer) {
      initPortalMap();
      if (!portalMapInstance) return;
    }

    portalMarkersLayer.clearLayers();
    portalCirclesLayer.clearLayers();

    const bounds = L.latLngBounds();
    let count = 0;
    const statusLabel = document.getElementById('portal-map-status');

    if (filterKey === 'lifestyle') {
      loadPoiRadarData(function (data) {
        if (!data || !data.projects) return;

        for (const key in data.projects) {
          const cluster = data.projects[key];
          if (cluster.lat && cluster.lon) {
            // 3km radius circle
            L.circle([cluster.lat, cluster.lon], {
              radius: 3000,
              color: '#059669',
              weight: 1.5,
              dashArray: '6, 6',
              fillColor: '#059669',
              fillOpacity: 0.04
            }).addTo(portalCirclesLayer);

            // Anchor marker
            const aIcon = L.divIcon({
              className: 'anchor-marker-refined',
              html: '<div style="background:#182842; border:2.5px solid #957B2B; color:#FFFFFF; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:14px; box-shadow:0 3px 10px rgba(0,0,0,0.3);">🏛️</div>',
              iconSize: [30, 30],
              iconAnchor: [15, 15]
            });

            const aMarker = L.marker([cluster.lat, cluster.lon], { icon: aIcon }).addTo(portalMarkersLayer);
            aMarker.on('click', (function (c) {
              return function () { window.openPropertyModal(c, 'anchor'); };
            })(cluster));

            bounds.extend([cluster.lat, cluster.lon]);
            count++;

            // Top POIs if populated
            if (Array.isArray(cluster.pois)) {
              cluster.pois.forEach(function (poi) {
                if (poi.lat && poi.lon) {
                  const catInfo = (data.categories && data.categories[poi.cat]) || { icon: '📍', color: '#182842' };
                  const pIcon = L.divIcon({
                    className: 'poi-custom-marker',
                    html: `<div style="background:#FFFFFF; border:2px solid ${catInfo.color}; width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:11px; box-shadow:0 2px 6px rgba(0,0,0,0.18);">${catInfo.icon}</div>`,
                    iconSize: [24, 24],
                    iconAnchor: [12, 12]
                  });

                  const pMarker = L.marker([poi.lat, poi.lon], { icon: pIcon }).addTo(portalMarkersLayer);
                  pMarker.on('click', (function (pItem, clItem) {
                    return function () {
                      pItem._cluster = clItem;
                      window.openPropertyModal(pItem, 'poi');
                    };
                  })(poi, cluster));

                  bounds.extend([poi.lat, poi.lon]);
                  count++;
                }
              });
            }
          }
        }

        if (statusLabel) {
          statusLabel.innerHTML = `Exibindo <strong>${count} pontos de conveniência e infraestrutura</strong> nos 8 clusters nobres de São Paulo (raio de 3 km).`;
        }

        if (count > 0 && portalMapInstance) {
          portalMapInstance.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 });
        }
      });
      return;
    }

    if (filterKey === 'concorrencia') {
      MARKET_COMPETITORS.forEach(function (comp) {
        if (comp.ll && comp.ll.length === 2 && comp.ll[0] !== 0) {
          const marker = L.marker(comp.ll, { icon: compIcon }).addTo(portalMarkersLayer);
          marker.on('click', function () {
            window.openPropertyModal(comp, 'concorrencia');
          });
          bounds.extend(comp.ll);
          count++;
        }
      });

      if (statusLabel) {
        statusLabel.innerHTML = `Exibindo <strong>${count} empreendimentos benchmark da concorrência</strong> de mercado (Cyrela, Trisul, Mitre, EZTEC, JFL Living) com comparativos de assimetria Lavvi.`;
      }
    } else {
      const list = getProjectsList();
      list.forEach(function (p) {
        let include = false;
        if (filterKey === 'todos') {
          include = true;
        } else if (filterKey === 'lancamentos') {
          include = (p.brand_line === 'lavvi' || !p.brand_line) && p.cat !== 'vendido' && (!p.status || !p.status.toLowerCase().includes('100% vendido'));
        } else if (filterKey === 'novvo') {
          include = (p.brand_line === 'novvo' || p.cat === 'novvo');
        } else if (filterKey === 'entregues') {
          include = (p.cat === 'vendido' || (p.status && p.status.toLowerCase().includes('100% vendido')));
        }

        if (include && p.ll && p.ll.length === 2 && p.ll[0] !== 0) {
          let icon = goldIcon;
          if (p.brand_line === 'novvo' || p.cat === 'novvo') {
            icon = novvoIcon;
          } else if (p.cat === 'vendido' || (p.status && p.status.toLowerCase().includes('100% vendido'))) {
            icon = historicoIcon;
          }

          const marker = L.marker(p.ll, { icon: icon }).addTo(portalMarkersLayer);
          marker.on('click', function () {
            window.openPropertyModal(p, 'projeto');
          });
          bounds.extend(p.ll);
          count++;
        }
      });

      if (statusLabel) {
        if (filterKey === 'todos') {
          statusLabel.innerHTML = `Exibindo o portfólio unificado de <strong>${count} empreendimentos</strong> da Lavvi e Linha Meu Novvo em São Paulo.`;
        } else if (filterKey === 'lancamentos') {
          statusLabel.innerHTML = `Exibindo <strong>${count} lançamentos e obras de alto padrão Lavvi</strong> ativos no mercado.`;
        } else if (filterKey === 'novvo') {
          statusLabel.innerHTML = `Exibindo <strong>${count} empreendimentos da Linha Meu Novvo</strong> (Smart Living com aviso legal sobre HIS/HMP).`;
        } else if (filterKey === 'entregues') {
          statusLabel.innerHTML = `Exibindo <strong>${count} empreendimentos 100% vendidos e entregues</strong> (Selo Histórico de Solvência e Pontualidade Grupo Cyrela).`;
        }
      }
    }

    if (count > 0 && portalMapInstance) {
      portalMapInstance.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 });
    }
  };

  // Official Verified Project Differentials
  function getProjectDifferentials(item) {
    const n = (item.nome || '').toLowerCase();
    if (n.includes('jardim da hípica') || n.includes('jardim da hipica')) {
      if (n.includes('apartment')) {
        return [
          'Torre E independente com tipologias compactas de 21 m² a 57 m²',
          'Minuta de convenção em cartório com liberação formal para locação short-stay/Airbnb',
          'Piscina com raia de 25m no 4º pavimento e infraestrutura completa'
        ];
      }
      return [
        'Terreno de 39.553 m² (~40.000 m²) + Praça Verde de 10.000 m² em frente ao CHSA',
        '02 Quadras de Tênis Oficiais (18x36m) + 02 Beach Tennis + Piscina com raia de 60m',
        'Gestão CBRE e Assessoria Esportiva Body Care inclusa no condomínio',
        '04 Private Houses independentes com piscina privativa e churrasqueira'
      ];
    }
    if (n.includes('t.o.m') || n.includes('tom paraíso') || n.includes('tom paraiso')) {
      return [
        'Terreno de 5.600 m² a 240m do Metrô Paraíso e 350m do HCor (+35 hospitais)',
        'Minuta de Convenção de Condomínio em cartório com liberação formal de Airbnb no R2V',
        'Design de interiores assinado por Triplex Arquitetura e lazer de resort completo',
        'Fluxo de obras com 47% durante a construção e 53% nas chaves'
      ];
    }
    if (n.includes('saffire')) {
      return [
        '1º Residencial da América Latina com interiores assinados por Elie Saab',
        'Terreno de 7.600 m² no quadrilátero nobre de Moema Pássaros (Av. Indianópolis)',
        'Residences de 360 m² e 493 m² (coberturas até 868 m²)'
      ];
    }
    if (n.includes('villa milano') || n.includes('villa studios') || n.includes('villa residence')) {
      return [
        'Assinado por Versace Home em Moema Pássaros (Av. Agami com Ibirapuera)',
        'Pronto para morar com unidades de 150 m² a 291 m² e Studios de 28 m² a 30 m²',
        'Acabamentos e áreas sociais com a grife italiana de luxo'
      ];
    }
    if (n.includes('petra')) {
      return [
        '1º Residencial do Mundo assinado por Boca do Lobo',
        'Terreno de 5.701 m² no Brooklin (a 350m da estação Metrô Brooklin)',
        'Plantas amplas de 162 m² e 199 m² (3 e 4 suítes com 2 a 3 vagas)'
      ];
    }
    if (n.includes('le six')) {
      return [
        'Serviços inclusos de Concierge CBRE e assessoria esportiva Body Care por 3 anos',
        'Terreno nobre no Paraíso/Ibirapuera com vedações convencionais sólidas',
        'Residences de 156 m² a 264 m² e Cobertura Duplex de 520 m²'
      ];
    }
    if (n.includes('heaven')) {
      return [
        'Design de prestígio mundial assinado pelo estúdio YOO (Philippe Starck)',
        'Localização privilegiada no Paraíso / Bela Vista (Rua Maestro Cardim)',
        'Residences de 187 e 258 m² com vista para a Paulista e Ibirapuera'
      ];
    }
    if (n.includes('soleil')) {
      return [
        'Design de interiores exclusivo assinado por Boca do Lobo na Chácara Klabin',
        'Residences de 246 m² com hall privativo e lazer de clube completo'
      ];
    }
    if (n.includes('well perdizes')) {
      return [
        'Terreno de 1.252 m² em Perdizes, a passos do campus da PUC-SP',
        'Alvenaria estrutural de alta eficiência e lazer moderno no rooftop',
        'Excelente liquidez de locação para estudantes, professores e médicos'
      ];
    }
    if (item.brand_line === 'novvo' || (item.cat && item.cat === 'novvo')) {
      return [
        'Smart Living planejado para alta rentabilidade de locação e mobilidade urbana',
        'Localização estratégica junto a estações e polos consolidados de transporte',
        'Áreas de lazer modernas com piscina, fitness, coworking e lavanderia coletiva'
      ];
    }
    if (item.cat === 'vendido' || (item.status && item.status.toLowerCase().includes('100% vendido'))) {
      return [
        'Patrimônio 100% entregue no prazo com a qualidade e solidez do Grupo Cyrela',
        'Histórico comprovado de valorização no mercado secundário de São Paulo',
        'Condomínio consolidado com gestão patrimonial e lazer de alto padrão'
      ];
    }
    return [
      'Padrão construtivo de excelência e solidez financeira do Grupo Cyrela (B3: LAVV3)',
      'Localização nobre em São Paulo com alta caminhabilidade e valorização',
      'Lazer de resort completo e arquitetura contemporânea'
    ];
  }

  function escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function setSafeAddress(addressEl, rawText) {
    if (!addressEl) return;
    addressEl.textContent = rawText;
    addressEl.innerHTML = escapeHTML(rawText);
  }

  // Accessibility: Background Inertness Controller
  function setBackgroundInert(isInert) {
    const backgroundElements = document.querySelectorAll(
      'header.site-header, #topo, aside.concierge-widget, footer.portal-footer, .hero-fullbleed, .catalog-section, .tools-hub-section, .advisor-section'
    );
    if (backgroundElements && typeof backgroundElements.forEach === 'function') {
      backgroundElements.forEach(function (el) {
        if (!el) return;
        if (isInert) {
          if (typeof el.setAttribute === 'function') {
            el.setAttribute('aria-hidden', 'true');
            el.setAttribute('inert', '');
          }
          try { el.inert = true; } catch (err) {}
        } else {
          if (typeof el.removeAttribute === 'function') {
            el.removeAttribute('aria-hidden');
            el.removeAttribute('inert');
          }
          try { el.inert = false; } catch (err) {}
        }
      });
    }
  }

  // Public Interface Contract 2: openPropertyModal(itemOrId, contextType)
  window.openPropertyModal = function (itemOrId, contextType) {
    let item = null;
    let type = contextType || 'projeto';

    if (typeof itemOrId === 'string') {
      const list = getProjectsList();
      item = list.find(function (p) {
        return p.nome && (p.nome.toLowerCase() === itemOrId.toLowerCase() || p.nome.toLowerCase().includes(itemOrId.toLowerCase()));
      });

      if (!item) {
        item = MARKET_COMPETITORS.find(function (c) {
          return c.nome && (c.nome.toLowerCase() === itemOrId.toLowerCase() || c.id === itemOrId);
        });
        if (item) type = 'concorrencia';
      }

      if (!item && cachedRadarData && cachedRadarData.projects) {
        for (const k in cachedRadarData.projects) {
          const cl = cachedRadarData.projects[k];
          if (cl.nome && cl.nome.toLowerCase().includes(itemOrId.toLowerCase())) {
            item = cl;
            type = 'anchor';
            break;
          }
          const pMatch = cl.pois && cl.pois.find(function (poi) {
            return (poi.nome && poi.nome.toLowerCase().includes(itemOrId.toLowerCase())) || poi.id === itemOrId;
          });
          if (pMatch) {
            item = pMatch;
            item._cluster = cl;
            type = 'poi';
            break;
          }
        }
      }
    } else {
      item = itemOrId;
    }

    if (!item) return;

    if (document.activeElement && typeof document.activeElement.focus === 'function') {
      previousActiveElement = document.activeElement;
    }

    renderModalContent(item, type);

    const overlay = document.getElementById('map-pin-modal-overlay');
    if (overlay) {
      overlay.style.display = 'flex';
      setBackgroundInert(true);
    }

    const card = document.getElementById('pin-modal-card');
    if (card && typeof card.focus === 'function') {
      card.setAttribute('tabindex', '-1');
      card.focus();
    }

    updateSchemaOrgStructuredData(item, type);
  };

  // Close Property Modal
  window.closePropertyModal = function () {
    const overlay = document.getElementById('map-pin-modal-overlay');
    if (overlay) overlay.style.display = 'none';
    setBackgroundInert(false);

    if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
      previousActiveElement.focus();
      previousActiveElement = null;
    }
  };

  // Render modal fields with verified data
  function renderModalContent(item, type) {
    const imgEl = document.getElementById('pin-modal-img');
    const badgesEl = document.getElementById('pin-modal-badges');
    const addressEl = document.getElementById('pin-modal-address');
    const titleEl = document.getElementById('pin-modal-title');
    const m2El = document.getElementById('pin-kpi-m2');
    const tipoEl = document.getElementById('pin-kpi-tipo');
    const precoEl = document.getElementById('pin-kpi-preco');
    const entregaEl = document.getElementById('pin-kpi-entrega');
    const diffHeadingEl = document.getElementById('pin-modal-diff-heading');
    const diffListEl = document.getElementById('pin-modal-diff-list');
    const legalBoxEl = document.getElementById('pin-modal-legal-box');
    const compBoxEl = document.getElementById('pin-modal-comp-box');
    const secondaryBtn = document.getElementById('pin-modal-secondary-btn');
    const waBtn = document.getElementById('pin-modal-wa-btn');

    if (!imgEl || !titleEl) return;

    // Reset dynamic boxes
    if (legalBoxEl) {
      legalBoxEl.style.display = 'none';
      legalBoxEl.innerHTML = '';
    }
    if (compBoxEl) {
      compBoxEl.style.display = 'none';
      compBoxEl.innerHTML = '';
    }

    if (type === 'concorrencia') {
      imgEl.src = item.hero_image || 'assets/images/jardim_hipica_facade_4k.jpg';
      imgEl.alt = item.nome;
      badgesEl.innerHTML = `
        <span class="pin-badge badge-comp">⚔️ Benchmark Concorrência</span>
        <span class="pin-badge">${item.incorporadora}</span>
        <span class="pin-badge">${item.status}</span>
      `;
      setSafeAddress(addressEl, `📍 ${item.endereco || item.bairro || 'São Paulo'}`);
      titleEl.innerText = item.nome;

      m2El.innerText = item.m2 || 'Sob Consulta';
      tipoEl.innerText = item.units || 'Residencial';
      precoEl.innerText = item.preco_m2 || item.preco_partida || 'Sob Consulta';
      entregaEl.innerText = item.entrega || item.status;

      diffHeadingEl.innerText = '🏢 Características do Concorrente';
      diffListEl.innerHTML = (item.diferenciais || []).map(function (d) { return `<li>${d}</li>`; }).join('');

      if (item.assimetria_lavvi && compBoxEl) {
        compBoxEl.style.display = 'block';
        compBoxEl.innerHTML = `<strong>⚔️ Análise de Assimetria vs. Lavvi:</strong> ${item.assimetria_lavvi}`;
      }

      secondaryBtn.innerText = 'Ver Catálogo Lavvi &rarr;';
      secondaryBtn.href = '#catalogo';
      secondaryBtn.onclick = function () { window.closePropertyModal(); };

      const waText = encodeURIComponent(`Olá Pedro! Vi a análise de benchmarking do ${item.nome} no mapa interativo e gostaria de entender as vantagens comparativas dos empreendimentos Lavvi.`);
      waBtn.href = `https://wa.me/5511966105952?text=${waText}`;
    } else if (type === 'poi') {
      const cluster = item._cluster || { nome: 'São Paulo', bairro: 'SP' };
      const catInfo = (cachedRadarData && cachedRadarData.categories && cachedRadarData.categories[item.cat]) || { label: 'Conveniência', icon: '📍' };
      imgEl.src = 'assets/images/jardim_hipica_facade_4k.jpg';
      imgEl.alt = item.nome;
      badgesEl.innerHTML = `
        <span class="pin-badge badge-poi">${catInfo.icon} ${catInfo.label}</span>
        <span class="pin-badge">${item.dist_km} km do Âncora</span>
      `;
      setSafeAddress(addressEl, `📍 ${item.endereco || cluster.bairro || 'São Paulo'}`);
      titleEl.innerText = item.nome;

      m2El.innerText = `${item.dist_km} km`;
      tipoEl.innerText = item.tipo || 'Ponto de Interesse';
      precoEl.innerText = `🚗 ${item.drive_min}m | 🚶 ${item.walk_min}m`;
      entregaEl.innerText = cluster.nome;

      diffHeadingEl.innerText = '📍 Destaques & Recomendações';
      const poiPoints = [];
      if (item.destaque) poiPoints.push(item.destaque);
      if (item.pedro_tip) poiPoints.push(`<strong>💡 Dica do Pedro Soares:</strong> ${item.pedro_tip}`);
      diffListEl.innerHTML = poiPoints.map(function (p) { return `<li>${p}</li>`; }).join('');

      if (item.website) {
        secondaryBtn.innerText = 'Site Oficial ↗';
        secondaryBtn.href = item.website;
        secondaryBtn.target = '_blank';
        secondaryBtn.onclick = null;
      } else {
        secondaryBtn.innerText = 'Explorar Radar 3km &rarr;';
        secondaryBtn.href = 'radar_mapa.html';
        secondaryBtn.target = '_self';
        secondaryBtn.onclick = null;
      }

      const waText = encodeURIComponent(`Olá Pedro! Vi a indicação do ${item.nome} no Radar 3km de ${cluster.nome} e gostaria de informações sobre imóveis nesta região.`);
      waBtn.href = `https://wa.me/5511966105952?text=${waText}`;
    } else if (type === 'anchor') {
      imgEl.src = 'assets/images/jardim_hipica_facade_4k.jpg';
      imgEl.alt = item.nome;
      badgesEl.innerHTML = `
        <span class="pin-badge badge-gold">🏛️ Empreendimento Âncora</span>
        <span class="pin-badge">Score ${item.lifestyle_score || 95} / 100</span>
      `;
      setSafeAddress(addressEl, `📍 ${item.endereco} • ${item.bairro}`);
      titleEl.innerText = item.nome;

      const sp = item.specs_oficiais || {};
      m2El.innerText = sp.tipologias || 'Consulte plantas';
      tipoEl.innerText = sp.terreno || 'Terreno Nobre';
      precoEl.innerText = sp.preco_partida || sp.preco_m2 || 'Tabela Vigente';
      entregaEl.innerText = sp.fluxo || 'Condição Exclusiva';

      diffHeadingEl.innerText = '✨ Especificações Oficiais de Empreendimento';
      const diffs = [];
      if (sp.lazer_destaque) diffs.push(sp.lazer_destaque);
      if (sp.gestao_servicos) diffs.push(sp.gestao_servicos);
      if (item.destaque_condominio) diffs.push(item.destaque_condominio);
      diffListEl.innerHTML = diffs.map(function (d) { return `<li>${d}</li>`; }).join('');

      secondaryBtn.innerText = 'Radar GIS Completo &rarr;';
      secondaryBtn.href = 'radar_mapa.html';
      secondaryBtn.target = '_self';
      secondaryBtn.onclick = null;

      const waText = encodeURIComponent(`Olá Pedro! Gostaria de receber o book e a tabela oficial de vendas do ${item.nome}.`);
      waBtn.href = `https://wa.me/5511966105952?text=${waText}`;
    } else {
      // Standard Project (Lavvi / Novvo / Vendido)
      imgEl.src = item.hero_image || 'assets/images/jardim_hipica_facade_4k.jpg';
      imgEl.alt = item.nome;

      let brandBadgeClass = 'badge-gold';
      let brandLabel = 'Lavvi Luxury';
      const isNovvo = (item.brand_line === 'novvo' || item.cat === 'novvo');
      const isVendido = (item.cat === 'vendido' || (item.status && item.status.toLowerCase().includes('100% vendido')));

      if (isNovvo) {
        brandBadgeClass = 'badge-novvo';
        brandLabel = 'Linha Meu Novvo';
      } else if (isVendido) {
        brandBadgeClass = 'badge-historico';
        brandLabel = '🏆 Selo Histórico de Entrega';
      }

      badgesEl.innerHTML = `
        <span class="pin-badge ${brandBadgeClass}">${brandLabel}</span>
        <span class="pin-badge">${item.status || 'Lançamento'}</span>
        ${item.data ? `<span class="pin-badge">${item.data}</span>` : ''}
      `;

      setSafeAddress(addressEl, `📍 ${item.bairro || 'São Paulo'} • São Paulo, SP`);
      titleEl.innerText = item.nome;

      m2El.innerText = item.m2 || 'Consulte tipologias';

      let tipoText = 'Sob Consulta';
      if (Array.isArray(item.units) && item.units.length > 0) {
        const plantas = item.units.map(function (u) { return u.planta; }).filter(Boolean);
        tipoText = Array.from(new Set(plantas)).slice(0, 3).join(' • ');
      } else if (isNovvo) {
        tipoText = 'Studios & 1 e 2 Dorms';
      } else if (isVendido) {
        tipoText = '100% Concluído & Entregue';
      }
      tipoEl.innerText = tipoText;

      let precoText = 'Tabela Vigente';
      if (item.avail_info) {
        precoText = item.avail_info;
      } else if (isVendido) {
        precoText = 'Totalmente Comercializado';
      }
      precoEl.innerText = precoText;

      let entregaText = item.data || item.entrega || 'Consulte';
      if (item.fluxo_curto) {
        entregaText += ` • ${item.fluxo_curto}`;
      }
      entregaEl.innerText = entregaText;

      diffHeadingEl.innerText = '✨ Diferenciais Exclusivos de Projeto';
      const diffs = getProjectDifferentials(item);
      diffListEl.innerHTML = diffs.map(function (d) { return `<li>${d}</li>`; }).join('');

      // Regulatory Notice
      if (isNovvo || item.nome.toLowerCase().includes('well perdizes')) {
        if (legalBoxEl) {
          legalBoxEl.style.display = 'block';
          legalBoxEl.innerHTML = `<strong>⚖️ Aviso Legal &amp; Política Habitacional:</strong> Conforme a legislação urbanística e habitacional de São Paulo, unidades enquadradas em HIS (Habitação de Interesse Social) e HMP (Habitação de Mercado Popular) têm expressa vedação legal e estatutária à exploração por Airbnb ou short-stay.`;
        }
      } else if (item.nome.toLowerCase().includes('t.o.m')) {
        if (legalBoxEl) {
          legalBoxEl.style.display = 'block';
          legalBoxEl.innerHTML = `<strong>⚖️ Convenção Auditada em Cartório:</strong> As unidades R2V (Livre) constam expressamente aprovadas para locação por temporada / Airbnb na Minuta de Convenção arquivada em cartório, blindando o investidor contra assembleias restritivas.`;
        }
      }

      if (item.tour_360) {
        secondaryBtn.innerText = '🌐 Tour Virtual 360° &rarr;';
        secondaryBtn.href = item.tour_360;
        secondaryBtn.target = '_blank';
        secondaryBtn.onclick = null;
      } else {
        secondaryBtn.innerText = 'Ver no Catálogo &rarr;';
        secondaryBtn.href = '#catalogo';
        secondaryBtn.target = '_self';
        secondaryBtn.onclick = function () { window.closePropertyModal(); };
      }

      const waText = encodeURIComponent(`Olá Pedro! Vi o ${item.nome} (${item.bairro}) no mapa interativo e gostaria de receber a apresentação oficial.`);
      waBtn.href = `https://wa.me/5511966105952?text=${waText}`;
    }
  }

  // Schema.org Structured Data Injector
  function updateSchemaOrgStructuredData(item, type) {
    let scriptEl = document.getElementById('schema-ld-json');
    if (!scriptEl) {
      scriptEl = document.createElement('script');
      scriptEl.id = 'schema-ld-json';
      scriptEl.type = 'application/ld+json';
      document.head.appendChild(scriptEl);
    }

    const agentSchema = {
      "@type": "RealEstateAgent",
      "@id": "https://lavvicollection.com.br/#pedro-soares",
      "name": "Pedro Soares | Lavvi Private Wealth",
      "alternateName": "Peter Corretor Lavvi Cyrela",
      "telephone": "+55-11-96610-5952",
      "url": "https://lavvicollection.com.br/",
      "image": "https://lavvicollection.com.br/assets/images/pedro_profile.jpg",
      "knowsLanguage": ["pt-BR", "en", "fr", "it", "es", "de"],
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "São Paulo",
        "addressRegion": "SP",
        "addressCountry": "BR"
      }
    };

    let propertySchema = null;
    if (type === 'concorrencia') {
      propertySchema = {
        "@type": ["ApartmentComplex", "Place"],
        "@id": `https://lavvicollection.com.br/#competitor-${item.id}`,
        "name": item.nome,
        "description": `${item.nome} em ${item.bairro}, São Paulo. Benchmark de mercado analisado pela Lavvi Private Wealth.`,
        "address": {
          "@type": "PostalAddress",
          "streetAddress": item.endereco || item.bairro,
          "addressLocality": "São Paulo",
          "addressRegion": "SP",
          "addressCountry": "BR"
        },
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": item.ll[0],
          "longitude": item.ll[1]
        }
      };
    } else if (type === 'poi') {
      propertySchema = {
        "@type": ["LocalBusiness", "Place"],
        "@id": `https://lavvicollection.com.br/#poi-${item.id}`,
        "name": item.nome,
        "description": `${item.tipo}${item.destaque ? ' — ' + item.destaque : ''}`,
        "address": {
          "@type": "PostalAddress",
          "streetAddress": item.endereco,
          "addressLocality": "São Paulo",
          "addressRegion": "SP",
          "addressCountry": "BR"
        },
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": item.lat,
          "longitude": item.lon
        }
      };
    } else {
      const lat = (item.ll && item.ll[0]) || item.lat || -23.575;
      const lon = (item.ll && item.ll[1]) || item.lon || -46.66;
      const isSoldOut = (item.cat === 'vendido' || (item.status && item.status.toLowerCase().includes('100% vendido')));
      let offerPrice = "Sob Consulta";
      if (item.avail_info) {
        offerPrice = item.avail_info;
      } else if (item.specs_oficiais && item.specs_oficiais.preco_partida) {
        offerPrice = item.specs_oficiais.preco_partida;
      } else if (item.preco_partida) {
        offerPrice = item.preco_partida;
      }

      propertySchema = {
        "@type": ["ApartmentComplex", "RealEstateListing", "Place"],
        "@id": `https://lavvicollection.com.br/#project-${encodeURIComponent((item.nome || '').toLowerCase().replace(/\s+/g, '-'))}`,
        "name": `${item.nome} Lavvi`,
        "description": `${item.nome} — Empreendimento ${item.brand_line === 'novvo' ? 'Linha Meu Novvo' : 'Lavvi'} no bairro ${item.bairro}, São Paulo. Curadoria exclusiva Pedro Soares.`,
        "url": item.url || "https://lavvicollection.com.br/",
        "image": item.hero_image || "https://lavvipublico.s3.amazonaws.com/lavvicombr/images/20b362e7-f04b-4a11-9387-137c3483da4f_1_perspectiva_ilustrada_da_fachada.webp",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": item.endereco || item.bairro,
          "addressLocality": "São Paulo",
          "addressRegion": "SP",
          "addressCountry": "BR"
        },
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": lat,
          "longitude": lon
        },
        "broker": {
          "@type": "RealEstateAgent",
          "@id": "https://lavvicollection.com.br/#pedro-soares",
          "name": "Pedro Soares | Lavvi Private Wealth",
          "telephone": "+55-11-96610-5952",
          "url": "https://lavvicollection.com.br/"
        },
        "seller": {
          "@id": "https://lavvicollection.com.br/#pedro-soares"
        },
        "offers": {
          "@type": "Offer",
          "priceCurrency": "BRL",
          "price": offerPrice,
          "availability": isSoldOut ? "https://schema.org/SoldOut" : "https://schema.org/InStock",
          "seller": {
            "@id": "https://lavvicollection.com.br/#pedro-soares"
          }
        }
      };
    }

    const payload = {
      "@context": "https://schema.org",
      "@graph": [agentSchema, propertySchema].filter(Boolean)
    };

    scriptEl.textContent = JSON.stringify(payload, null, 2);
  }

  // Keyboard Controller: ESC and Focus Trap (Tab / Shift+Tab)
  document.addEventListener('keydown', function (e) {
    const overlay = document.getElementById('map-pin-modal-overlay');
    const isModalOpen = overlay && overlay.style.display !== 'none';
    if (!isModalOpen) return;

    if (e.key === 'Escape') {
      window.closePropertyModal();
      return;
    }

    if (e.key === 'Tab') {
      if (typeof overlay.querySelectorAll === 'function') {
        const focusableElements = overlay.querySelectorAll(
          'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        if (focusableElements && focusableElements.length > 0) {
          const firstElement = focusableElements[0];
          const lastElement = focusableElements[focusableElements.length - 1];

          if (e.shiftKey) {
            if (
              document.activeElement === firstElement ||
              document.activeElement === overlay ||
              document.activeElement === document.getElementById('pin-modal-card')
            ) {
              if (typeof lastElement.focus === 'function') {
                e.preventDefault();
                lastElement.focus();
              }
            }
          } else {
            if (document.activeElement === lastElement) {
              if (typeof firstElement.focus === 'function') {
                e.preventDefault();
                firstElement.focus();
              }
            }
          }
        }
      }
    }
  });

  // Modal Backdrop Click to Close
  document.addEventListener('DOMContentLoaded', function () {
    const overlayEl = document.getElementById('map-pin-modal-overlay');
    if (overlayEl) {
      overlayEl.addEventListener('click', function (e) {
        if (e.target.id === 'map-pin-modal-overlay') {
          window.closePropertyModal();
        }
      });
    }

    // Auto-init if container present
    if (document.getElementById('portal-map')) {
      initPortalMap();
    }
  });

})();
