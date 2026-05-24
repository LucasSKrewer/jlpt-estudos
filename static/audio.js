(function () {
    "use strict";

    if (!("speechSynthesis" in window)) {
        document.querySelectorAll(".btn-play").forEach(function (b) { b.hidden = true; });
        return;
    }

    var synth = window.speechSynthesis;
    var vozJp = null;
    var vozResolvida = false;

    function escolherVozJp() {
        var vozes = synth.getVoices();
        if (!vozes || vozes.length === 0) return null;

        var jp = vozes.filter(function (v) { return v.lang && v.lang.toLowerCase().indexOf("ja") === 0; });
        if (jp.length === 0) return null;

        var preferidas = ["Haruka", "Ayumi", "Sayaka", "Kyoko", "Otoya", "Google", "Microsoft"];
        for (var i = 0; i < preferidas.length; i++) {
            for (var j = 0; j < jp.length; j++) {
                if (jp[j].name.indexOf(preferidas[i]) !== -1) return jp[j];
            }
        }
        return jp[0];
    }

    function resolverVoz() {
        if (vozResolvida) return;
        var vozes = synth.getVoices();
        if (!vozes || vozes.length === 0) return;
        vozJp = escolherVozJp();
        vozResolvida = true;
    }

    resolverVoz();
    if (typeof synth.onvoiceschanged !== "undefined") {
        synth.addEventListener("voiceschanged", function () {
            resolverVoz();
            atualizarBotoes();
        });
    }

    function atualizarBotoes() {
        var botoes = document.querySelectorAll(".btn-play");
        if (vozJp === null && vozResolvida) {
            botoes.forEach(function (b) {
                b.disabled = true;
                b.title = "Voz japonesa indisponível neste navegador";
            });
            mostrarAvisoSemVoz();
        } else {
            botoes.forEach(function (b) {
                b.disabled = false;
                b.title = "Ouvir pronúncia";
            });
        }
    }

    function mostrarAvisoSemVoz() {
        if (document.getElementById("aviso-sem-voz-jp")) return;
        var aviso = document.createElement("div");
        aviso.id = "aviso-sem-voz-jp";
        aviso.className = "flash flash-info";
        aviso.textContent = "Nenhuma voz em japonês foi encontrada neste navegador. No Windows, adicione o pacote de idiomas japonês em Configurações > Hora e Idioma > Idioma. Os botões de áudio ficarão disponíveis em seguida.";
        var main = document.querySelector("main");
        if (main) main.insertBefore(aviso, main.firstChild);
    }

    function falar(texto) {
        if (!texto) return;
        if (vozJp === null) {
            resolverVoz();
            if (vozJp === null) return;
        }
        synth.cancel();
        var utt = new SpeechSynthesisUtterance(texto);
        utt.voice = vozJp;
        utt.lang = vozJp.lang || "ja-JP";
        utt.rate = 0.9;
        utt.pitch = 1.0;
        synth.speak(utt);
    }

    document.addEventListener("click", function (ev) {
        var alvo = ev.target.closest(".btn-play");
        if (!alvo) return;
        ev.preventDefault();
        var texto = alvo.getAttribute("data-fala");
        falar(texto);
    });

    document.addEventListener("DOMContentLoaded", function () {
        setTimeout(function () {
            resolverVoz();
            atualizarBotoes();
        }, 200);
    });
})();
