document.getElementById("analizBtn").addEventListener("click", async () => {
  const loading = document.getElementById("loading");
  const sonuc = document.getElementById("sonuc");
  loading.classList.remove("hidden");
  sonuc.innerText = "";

  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: () => {
        const infoList = Array.from(document.querySelectorAll(".classifiedInfoList li"))
          .map(li => li.innerText.trim())
          .join("\n");

        const aciklama = document.getElementById("classifiedDescription")?.innerText.trim() || "";
        const metin = `İlan Bilgileri:\n${infoList}\n\nAçıklama:\n${aciklama}`;
        


        return { metin };
      }
    }, async (results) => {
      const { metin } = results[0].result;
      console.log("Gönderilen metin:", metin);

      try {
        const response = await fetch("http://localhost:8000/evaluate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ metin })
        });

        const result = await response.json();
        sonuc.innerText = `Puan: ${result.puan}\n\n${result.yorum}`;
      } catch (err) {
        sonuc.innerText = "❌ Sunucuya bağlanılamadı.";
        console.error("Fetch hatası:", err);
      } finally {
        loading.classList.add("hidden");
      }
    });
  });
});
