(() => {
  const title = document.querySelector(".classifiedTitle")?.innerText || "";
  const infoList = document.querySelectorAll(".classifiedInfoList li");
  const description = document.querySelector("#classifiedDescription")?.innerText || "";

  let data = {
    baslik: title,
    yil: null,
    km: null,
    boyali: false,
    agir_hasar: false,
    aciklama: description
  };

  infoList.forEach(li => {
    const text = li.innerText.toLowerCase();
    if (text.includes("yıl")) data.yil = parseInt(text.replace(/\D/g, ""));
    if (text.includes("km")) data.km = parseInt(text.replace(/\D/g, ""));
    if (text.includes("boya")) data.boyali = true;
    if (text.includes("hasar")) data.agir_hasar = true;
  });

  window.postMessage({ type: "ILAN_VERISI", data }, "*");
})();
