const ciudades = [
    "Bourg-en-Bresse", "Laon", "Moulins", "Digne-les-Bains", "Gap", "Nice",
    "Privas", "Charleville-Mézières", "Foix", "Troyes", "Carcassonne",
    "Rodez", "Marseille", "Caen", "Aurillac", "Angoulême", "La Rochelle",
    "Bourges", "Tulle", "Ajaccio", "Bastia", "Dijon", "Saint-Brieuc",
    "Guéret", "Périgueux", "Besançon", "Valence", "Évreux", "Chartres",
    "Quimper", "Nîmes", "Toulouse", "Auch", "Bordeaux", "Montpellier",
    "Rennes", "Châteauroux", "Tours", "Grenoble", "Lons-le-Saunier",
    "Mont-de-Marsan", "Blois", "Saint-Étienne", "Le Puy-en-Velay",
    "Nantes", "Orléans", "Cahors", "Agen", "Mende", "Angers", "Saint-Lô",
    "Châlons-en-Champagne", "Chaumont", "Laval", "Nancy", "Bar-le-Duc",
    "Vannes", "Metz", "Nevers", "Lille", "Beauvais", "Alençon", "Arras",
    "Clermont-Ferrand", "Pau", "Tarbes", "Perpignan", "Strasbourg",
    "Colmar", "Lyon", "Vesoul", "Mâcon", "Le Mans", "Chambéry", "Annecy",
    "Paris", "Rouen", "Melun", "Versailles", "Niort", "Amiens", "Albi",
    "Montauban", "Toulon", "Avignon", "La Roche-sur-Yon", "Poitiers",
    "Limoges", "Épinal", "Auxerre", "Belfort", "Évry-Courcouronnes",
    "Nanterre", "Bobigny", "Créteil", "Cergy"
]

// const csvTexto = `
// 0,39
// 0,69
// 0,71
// 0,74
// 1,7
// 1,51
// 1,59
// 1,60
// 1,62
// 1,77
// 1,80
// 1,93
// 1,95
// 2,17
// 2,23
// 2,58
// 2,63
// 2,69
// 2,71
// 3,4
// 3,5
// 3,83
// 3,84
// 4,5
// 4,6
// 4,26
// 4,38
// 4,84
// 5,19
// 5,20
// 5,83
// 6,26
// 6,42
// 6,43
// 6,48
// 6,84
// 7,51
// 7,55
// 7,57
// 7,59
// 8,10
// 8,31
// 8,65
// 8,66
// 9,51
// 9,52
// 9,55
// 9,77
// 9,89
// 10,31
// 10,34
// 10,66
// 10,81
// 11,14
// 11,34
// 11,46
// 11,48
// 11,81
// 11,82
// 12,30
// 12,83
// 12,84
// 13,27
// 13,50
// 13,61
// 13,76
// 14,18
// 14,43
// 14,46
// 14,48
// 14,63
// 15,16
// 15,24
// 15,33
// 15,79
// 15,86
// 15,87
// 16,33
// 16,79
// 16,85
// 17,23
// 17,36
// 17,37
// 17,41
// 17,45
// 17,58
// 17,89
// 18,23
// 18,24
// 18,63
// 18,87
// 19,20
// 19,83
// 20,83
// 21,25
// 21,39
// 21,52
// 21,58
// 21,70
// 21,89
// 22,29
// 22,35
// 22,50
// 22,56
// 23,36
// 23,63
// 23,86
// 23,87
// 24,33
// 24,46
// 24,47
// 24,87
// 25,39
// 25,70
// 26,38
// 26,42
// 26,84
// 27,28
// 27,61
// 27,76
// 27,95
// 28,45
// 28,72
// 28,78
// 29,35
// 29,56
// 30,34
// 30,48
// 30,84
// 31,32
// 31,65
// 31,81
// 31,82
// 32,40
// 32,47
// 32,65
// 32,82
// 33,40
// 33,47
// 34,48
// 34,66
// 35,44
// 35,49
// 35,50
// 35,53
// 35,56
// 36,37
// 36,41
// 36,86
// 37,41
// 37,49
// 37,72
// 37,86
// 38,69
// 38,73
// 39,71
// 39,89
// 40,47
// 40,64
// 41,45
// 42,43
// 42,63
// 42,69
// 43,48
// 43,63
// 44,49
// 44,56
// 44,79
// 44,85
// 45,89
// 45,91
// 46,47
// 46,81
// 46,82
// 47,82
// 49,53
// 49,72
// 49,79
// 49,85
// 49,86
// 50,53
// 50,61
// 51,55
// 51,77
// 51,93
// 51,94
// 52,55
// 52,70
// 52,88
// 53,61
// 53,72
// 54,55
// 54,57
// 54,67
// 54,88
// 55,57
// 57,67
// 57,88
// 58,89
// 59,62
// 60,76
// 60,80
// 60,95
// 61,72
// 62,80
// 63,69
// 64,65
// 67,68
// 67,88
// 68,88
// 68,90
// 69,71
// 69,73
// 70,88
// 70,90
// 71,89
// 73,74
// 75,77
// 75,78
// 75,91
// 75,92
// 75,93
// 75,94
// 75,95
// 76,80
// 77,89
// 77,91
// 77,94
// 78,91
// 78,92
// 78,94
// 78,95
// 79,85
// 79,86
// 80,95
// 81,82
// 86,87
// 88,90
// 91,94
// 92,93
// 92,95
// 93,94
// `;

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function setReactInputValue(input, value) {
  const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype,
    "value"
  ).set;

  nativeInputValueSetter.call(input, value);

  input.dispatchEvent(new Event("input", { bubbles: true }));
  input.dispatchEvent(new Event("change", { bubbles: true }));
}

function obtenerInputs() {
  const inputs = [...document.querySelectorAll("input")]
    .filter(input => {
      const style = window.getComputedStyle(input);
      return (
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        !input.disabled &&
        input.offsetParent !== null
      );
    });

  // console.log("Inputs encontrados:", inputs);

  return {
    inputOrigen: inputs[0],
    inputDestino: inputs[1]
  };
}

async function escribirYSeleccionar(input, valor) {
  input.focus();

  input.value = "";
  setReactInputValue(input, "");

  await sleep(500);

  setReactInputValue(input, valor);

  await sleep(1000);
    input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));
    await sleep(100);
    input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));
        await sleep(100);

        input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));
        await sleep(100);

        input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));    await sleep(100);

        input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));    await sleep(100);

        input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));    await sleep(100);

        input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));    await sleep(100);

        input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));    await sleep(100);

        input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));    await sleep(100);

        input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "ArrowUp",
    code: "ArrowUp",
    keyCode: 38,
    which: 38,
    bubbles: true
    }));
//   await sleep(300);
//     input.dispatchEvent(new KeyboardEvent("keydown", {
//     key: "ArrowDown",
//     code: "ArrowDown",
//     keyCode: 40,
//     which: 40,
//     bubbles: true
//   }));



  await sleep(300);

  input.dispatchEvent(new KeyboardEvent("keydown", {
    key: "Enter",
    code: "Enter",
    keyCode: 13,
    which: 13,
    bubbles: true
  }));

  await sleep(1200);
}

function leerParesDesdeTextoCSV(csvTexto) {
  const lineas = csvTexto
    .split(/\r?\n/)
    .map(linea => linea.trim())
    .filter(Boolean);

  return lineas.map((linea, i) => {
    const partes = linea.split(",").map(x => x.trim());

    if (partes.length < 2) {
      throw new Error(`Fila inválida ${i + 1}: ${linea}`);
    }

    const origenIndice = Number(partes[0]);
    const destinoIndice = Number(partes[1]);

    if (Number.isNaN(origenIndice) || Number.isNaN(destinoIndice)) {
      throw new Error(`Fila inválida ${i + 1}: ${linea}`);
    }

    return {
      fila: i + 1,
      origenIndice,
      destinoIndice
    };
  });
}

function extraerDatosRuta() {
  const textoOriginal = document.body.innerText;

  const texto = textoOriginal
    .replace(/\u00A0/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  const distanciaMatch = texto.match(
    /(\d+(?:[.,]\d+)?\s*km)\s+de voyage/i
  );

  const conduiteMatch = texto.match(
    /((?:\d{1,2}\s*h\s*\d{1,2})|(?:\d{1,3}\s*min))\s+de conduite/i
  );

  const peageMatch = texto.match(
    /([\d.,]+\s*€)\s+(?:estimation\s*)?p[ée]age/i
  );

  return {
    resumen: {
      de_voyage: distanciaMatch
        ? distanciaMatch[1].replace(/\s+/g, "")
        : "",

      de_conduite: conduiteMatch
        ? conduiteMatch[1].replace(/\s+/g, "")
        : "",

      estimation_peage: peageMatch
        ? peageMatch[1].trim()
        : ""
    },

    textoCompleto: texto
  };
}

function convertirResultadosACSVConIndices(resultados) {
  const headers = [
    "origen_indice",
    "destino_indice",
    "origen",
    "destino",
    "de_voyage",
    "de_conduite",
    "estimation_peage",
    "estado"
  ];

  const escapeCSV = value => {
    if (value === null || value === undefined) return "";
    const str = String(value);
    return `"${str.replaceAll('"', '""')}"`;
  };

  const lineas = [
    headers.join(","),
    ...resultados.map(row =>
      headers.map(header => escapeCSV(row[header])).join(",")
    )
  ];

  return lineas.join("\n");
}

function descargarCSV(nombreArchivo, contenido) {
  const blob = new Blob([contenido], {
    type: "text/csv;charset=utf-8;"
  });

  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");

  a.href = url;
  a.download = nombreArchivo;

  document.body.appendChild(a);
  a.click();

  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

async function ejecutarRutasDesdeVariableCSV({
  csvTexto,
  ciudades,
  indiceBase = 0,
  pausaEntreRutas = 7000,
  pausaActualizacion = 7000,
  limite = null
}) {
  let pares = leerParesDesdeTextoCSV(csvTexto);

  if (limite !== null) {
    pares = pares.slice(0, limite);
  }

  // console.log("Pares leídos:");
  // console.table(pares);

  const resultados = [];

  for (let i = 0; i < pares.length; i++) {
    const par = pares[i];

    const posicionOrigen = par.origenIndice - indiceBase;
    const posicionDestino = par.destinoIndice - indiceBase;

    const origen = ciudades[posicionOrigen];
    const destino = ciudades[posicionDestino];

    if (!origen || !destino) {
      console.error("Índice fuera de rango:", par);

      resultados.push({
        origen_indice: par.origenIndice,
        destino_indice: par.destinoIndice,
        origen: origen || "",
        destino: destino || "",
        de_voyage: "",
        de_conduite: "",
        estimation_peage: "",
        estado: "ERROR_INDICE"
      });

      continue;
    }

    console.log(
      `Procesando ${i + 1}/${pares.length}: ${par.origenIndice} ${origen} → ${par.destinoIndice} ${destino}`
    );

    try {
      const { inputOrigen, inputDestino } = obtenerInputs();

      if (!inputOrigen || !inputDestino) {
        throw new Error("No se encontraron los inputs de origen y destino.");
      }

      await escribirYSeleccionar(inputOrigen, origen);
      await escribirYSeleccionar(inputDestino, destino);

      // console.log("Esperando actualización automática de la ruta...");
      await sleep(pausaActualizacion);

      const extraido = extraerDatosRuta();
      const resumen = extraido.resumen || {};

      resultados.push({
        origen_indice: par.origenIndice,
        destino_indice: par.destinoIndice,
        origen,
        destino,
        de_voyage: resumen.de_voyage || "",
        de_conduite: resumen.de_conduite || "",
        estimation_peage: resumen.estimation_peage || "",
        estado: "OK"
      });

    //   // console.log("Resultado guardado:");
    //   console.table([resultados[resultados.length - 1]]);

    } catch (error) {
      console.error(`Error en ruta ${origen} → ${destino}:`, error);

      resultados.push({
        origen_indice: par.origenIndice,
        destino_indice: par.destinoIndice,
        origen,
        destino,
        de_voyage: "",
        de_conduite: "",
        estimation_peage: "",
        estado: "ERROR"
      });
    }

    await sleep(pausaEntreRutas);
  }

  console.log("RESULTADOS FINALES:");
  console.table(resultados);

  const csvFinal = convertirResultadosACSVConIndices(resultados);

  descargarCSV("resultados_vinci_indices.csv", csvFinal);

  console.log("Descargado: resultados_vinci_indices.csv");

  return resultados;
}

