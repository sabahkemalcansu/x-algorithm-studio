# x-algorithm-studio

**Çalıştır · Anla · Geliştir**

> Tek tıkla X’in **public** For You (Phoenix) demosunun nasıl sıraladığını gör —  
> **veya** bu repoyu Claude / Cursor / Codex / Grok’a at; agent öğrensin, üstüne geliştirsin.

X / xAI ile resmi bağlantımız yok.  
Canlı timeline veya production weight iddiası yok.  
[`xai-org/x-algorithm`](https://github.com/xai-org/x-algorithm) üzerine kurulu (Apache-2.0).

## Hızlı başlangıç (offline, 2 dk)

```bash
cd x-algorithm-studio
make doctor
make demo-fixture
make open
```

`out/latest/report.html` → sade aha raporu.

## Tam model demosu

```bash
make vendor && make pull && make demo-native && make open
```

~3GB artifact + git-lfs gerekir.

## Agent’a at

[`agent/PROMPT_DROP_IN.md`](agent/PROMPT_DROP_IN.md) içeriğini yapıştır.  
Önce `AGENTS.md` ve `docs/curriculum.md`.

## Vaad

İndir → anla → istersen geliştir.  
“Tweetler neden üste çıkar?” sorusuna **mekanizma** cevabı; garanti viral formülü değil.
