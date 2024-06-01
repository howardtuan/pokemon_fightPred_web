let pokemonData = [];

function parseCSV(str) {
  const lines = str.split("\n");
  const result = [];
  for (let i = 1; i < lines.length; i++) {
    const currentLine = lines[i].split(",");
    if (currentLine.length > 1) { // 確保有足夠的列
      result.push({ id: currentLine[0], name: currentLine[1] });
    }
  }
  return result;
}

function fetchDataAndInitAutocomplete() {
  fetch('/static/pokemon_withoutMEGA.csv')  // 使用相對路徑指向上一層資料夾的CSV檔案
    .then(response => response.text())
    .then(data => {
      pokemonData = parseCSV(data);
      const pokemonList = pokemonData.map(pokemon => pokemon.name);
      autocomplete(document.getElementById("pokemonInput1"), pokemonList);
      autocomplete(document.getElementById("pokemonInput2"), pokemonList);
    })
    .catch(error => console.error('Error fetching the CSV file:', error));
}

function autocomplete(inp, arr) {
  let currentFocus;

  inp.addEventListener("input", function(e) {
    let a, b, i, val = this.value;
    closeAllLists();
    if (!val) { return false;}
    currentFocus = -1;
    a = document.createElement("DIV");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    this.parentNode.appendChild(a);
    for (i = 0; i < arr.length; i++) {
      if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        b = document.createElement("DIV");
        b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
        b.innerHTML += arr[i].substr(val.length);
        b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
        b.addEventListener("click", function(e) {
          inp.value = this.getElementsByTagName("input")[0].value;
          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });

  inp.addEventListener("keydown", function(e) {
    let x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      currentFocus++;
      addActive(x);
    } else if (e.keyCode == 38) {
      currentFocus--;
      addActive(x);
    } else if (e.keyCode == 13) {
      e.preventDefault();
      if (currentFocus > -1) {
        if (x) x[currentFocus].click();
      }
    }
  });

  function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    x[currentFocus].classList.add("autocomplete-active");
  }

  function removeActive(x) {
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }

  function closeAllLists(elmnt) {
    let x = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }

  document.addEventListener("click", function (e) {
    closeAllLists(e.target);
  });
}

function handleFight() {
  const pokemon1 = document.getElementById("pokemonInput1").value;
  const pokemon2 = document.getElementById("pokemonInput2").value;

  const pokemon1Data = pokemonData.find(p => p.name && p.name.toLowerCase() === pokemon1.toLowerCase());
  const pokemon2Data = pokemonData.find(p => p.name && p.name.toLowerCase() === pokemon2.toLowerCase());

  if (!pokemon1Data || !pokemon2Data) {
    alert('One or both Pokémon not found!');
    return;
  }

  const form = document.getElementById("fightForm");
  const pokemon1IdInput = document.createElement("input");
  pokemon1IdInput.setAttribute("type", "hidden");
  pokemon1IdInput.setAttribute("name", "pokemon1_id");
  pokemon1IdInput.setAttribute("value", pokemon1Data.id);

  const pokemon2IdInput = document.createElement("input");
  pokemon2IdInput.setAttribute("type", "hidden");
  pokemon2IdInput.setAttribute("name", "pokemon2_id");
  pokemon2IdInput.setAttribute("value", pokemon2Data.id);

  form.appendChild(pokemon1IdInput);
  form.appendChild(pokemon2IdInput);

  form.submit();
}

// 初始化動態提示功能
fetchDataAndInitAutocomplete();
