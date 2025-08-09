```markdown
Scroll down to see the `ENGLISH README`

# TikTok FPS Compression Bypasser

## Sobre o projeto

O TikTok limita a taxa máxima de FPS dos vídeos a 30 fps por padrão, utilizando um **hardware encoder** para acelerar o vídeo internamente. Esse encoder ajusta o tempo do vídeo com base no parâmetro `timescale` presente nos átomos internos do arquivo MP4 (`mvhd` e `mdhd`). O vídeo final é exibido na taxa de quadros original, mas essa aceleração depende diretamente do valor do `timescale`.

Como faço edições no TikTok e quero que minhas edições sejam vistas a 60 fps, criei este método para burlar a compressão automática do TikTok, ajustando diretamente o `timescale` do arquivo para "enganar" o encoder e manter a fluidez original.

## Avisos Importantes

Com este método, é possível postar vídeos com FPS **ilimitado**, ultrapassando o limite padrão de 30 fps do TikTok. 

No entanto, o **playback** desses vídeos vai depender totalmente da potência do hardware do dispositivo do usuário e do decoder do celular. Ou seja, embora o arquivo tenha uma taxa de quadros maior, em dispositivos mais fracos o vídeo pode não rodar suavemente.

Resumindo: o FPS do vídeo no arquivo é ilimitado, mas a reprodução real pode variar conforme o dispositivo.

Recomendação: usar no máximo 120 fps originais.


---

## Histórico e Inspiração

O método antigo de burlar FPS via upload caiu no dia **14 de março de 2025**, e foi aí que comecei a criar um método novo.

De início, minha inspiração era tentar fazer um remake do método do @nxt_shark537 no TikTok. Na época, eu não sabia como ele fez o método dele e não tinha pistas nenhuma. Hoje sei que ele usou ffmpeg para isso. ( ffmpeg -itsscale 2 -i input.mp4 -c:v copy -c:a copy output.mp4) 

Como eu não sabia disso na época, acabei indo por um caminho diferente, focando na modificação dos metadados internos do arquivo MP4. Enquanto o método do nxt_shark537 é feito com ffmpeg, o meu método atua diretamente nos átomos `mvhd` e `mdhd` do arquivo.

---

## Como funciona o método

O vídeo tem uma taxa de quadros original (por exemplo, 60 fps). O TikTok tenta forçar essa taxa para 30 fps usando um encoder de hardware que acelera o vídeo para caber nesse limite.

Para contornar isso, o script modifica o valor do `timescale` dentro dos átomos MP4 `mvhd` e `mdhd` com a fórmula:

```

Novo timescale = timescale original × (30 / FPS original do vídeo)

````

Dessa forma, o vídeo é acelerado proporcionalmente para manter a fluidez original mesmo com a compressão do TikTok.

---

## Sobre o slow motion no TikTok Web

É importante notar que, no **TikTok Web (navegador)**, os vídeos com este patch podem aparecer em **slow motion**. Isso acontece porque a versão web do TikTok utiliza um **software encoder**, que não interpreta o `timescale` da mesma forma que o hardware encoder dos apps móveis.

Portanto, para ver o efeito completo, recomendo assistir seus vídeos editados via **app móvel do TikTok**.

---

## Uso

1. Clone ou baixe este repositório.  
2. Execute o script via terminal:
    python3 patcher.py input.mp4 output.mp4 [scale_factor]
````

* `input.mp4`: arquivo de vídeo original.
* `output.mp4`: arquivo modificado.
* `scale_factor` (opcional): fator para ajustar manualmente o timescale (ex: 1.5). Se não fornecido, o script calcula automaticamente baseado na fórmula: (30 / FPS original do vídeo)

---

## Créditos

* [Lenoz7](https://www.tiktok.com/@lenoz7) (Luís) — Criador do projeto e script, responsável pelo início do desenvolvimento.
* [Poshyler](https://www.tiktok.com/@poshyler) — Amigo e colaborador que ajudou a desenvolver a ideia e a implementação técnica.
* [nxt_shark537](https://www.tiktok.com/@nxt_shark537) — Inspiração para o conceito do método; não participou do desenvolvimento, apenas o conceito foi aproveitado.

---
```
## Licença

Este projeto é **open source** e você pode usar, modificar e contribuir livremente.

```
---------------------------------------------------
ENGLISH README
---------------------------------------------------
```markdown
# TikTok FPS Compression Bypasser

## About the project

TikTok limits the maximum FPS of videos to 30 fps by default, using a **hardware encoder** to internally speed up the video. This encoder adjusts the video timing based on the `timescale` parameter found in the internal atoms of the MP4 file (`mvhd` and `mdhd`). The final video is displayed at the original frame rate, but this speedup depends directly on the value of the `timescale`.

Since I make edits on TikTok and want my edits to be seen at 60 fps, I created this method to bypass TikTok’s automatic compression by directly adjusting the file’s `timescale` to "trick" the encoder and keep the original smoothness.

## Important Notices

With this method, it is possible to upload videos with **unlimited** FPS, surpassing TikTok’s standard 30 fps limit.

However, the **playback** of these videos will depend entirely on the hardware power of the user’s device and the phone’s decoder. So, even though the file has a higher frame rate, on weaker devices the video might not play smoothly.

In summary: the FPS in the video file is unlimited, but the actual playback may vary depending on the device.

Recommendation: use a maximum of 120 fps original.

---

## History and Inspiration

The old method to bypass FPS via upload stopped working on **March 14, 2025**, and that’s when I started creating a new method.

Initially, my inspiration was to try to remake @nxt_shark537’s TikTok method. At the time, I didn’t know how he did his method and had no clues. Today I know he used ffmpeg for that. ( ffmpeg -itsscale 2 -i input.mp4 -c:v copy -c:a copy output.mp4) 

Since I didn’t know that at the time, I went a different path, focusing on modifying the internal metadata of the MP4 file. While nxt_shark537’s method is done with ffmpeg, my method works directly on the `mvhd` and `mdhd` atoms of the file.

---

## How the method works

The video has an original frame rate (for example, 60 fps). TikTok tries to force this rate to 30 fps using a hardware encoder that speeds up the video to fit this limit.

To circumvent this, the script modifies the `timescale` value inside the MP4 `mvhd` and `mdhd` atoms with the formula:

```

New timescale = original timescale × (30 / original FPS of the video)

```

This way, the video is proportionally sped up to keep the original smoothness despite TikTok’s compression.

---

## About slow motion on TikTok Web

It is important to note that on **TikTok Web (browser)**, videos with this patch might appear in **slow motion**. This happens because TikTok’s web version uses a **software encoder**, which does not interpret the `timescale` the same way the hardware encoder in mobile apps does.

Therefore, to see the full effect, I recommend watching your edited videos via the **TikTok mobile app**.

---

## Usage

1. Clone or download this repository.  
2. Run the script via terminal:
    python3 patcher.py input.mp4 output.mp4 [scale_factor]
```

* `input.mp4`: original video file.
* `output.mp4`: modified file.
* `scale_factor` (optional): factor to manually adjust the timescale (ex: 1.5). If not provided, the script calculates automatically based on the formula: (30 / original FPS of the video)

---

## Credits

* [Lenoz7](https://www.tiktok.com/@lenoz7) (Luís) — Creator of the project and script, responsible for the start of development.
* [Poshyler](https://www.tiktok.com/@poshyler) — Friend and collaborator who helped develop the idea and technical implementation.
* [nxt\_shark537](https://www.tiktok.com/@nxt_shark537) — Inspiration for the method’s concept; did not participate in development, only the concept was used.

---

```
## License

This project is **open source** and you can use, modify, and contribute freely.

```

