---
id: project-naptha
name: Project Naptha
description: Browser extension that lets users highlight, copy, edit, and translate text inside images.
domain: ai-ml
tags: [browser-extension, ocr, college-hackathon]
event:
  name: HackMIT
  year: 2013
links:
  official: https://www.projectnaptha.com/
evidence:
  - url: https://en.wikipedia.org/wiki/HackMIT
    supports: "HackMIT 2013 origin"
deep_dive: true
key_idea: >-
  Run OCR locally, then lay invisible text over the image so the recognized words behave like real text.
learn_from: >-
  The model is not the product. The product is making the output act like the interface people already know.
verified_at: 2026-10-24
---

## What it does

Project Naptha is a browser extension that makes text inside images selectable, copyable, editable, and translatable. You drag over a screenshot or a meme as if it were a document, and the words come out.

## The key insight

Optical character recognition was not new in 2013. The insight was placement. Once the engine returns words with bounding boxes, the extension can position transparent text elements directly over the image. From that point, the browser's own selection, copy, and translation features do the rest.

The interface is the trick. Users do not learn a new tool. They use the selection behavior they already have.

## How it works

The extension captures the image, draws it to a canvas, and runs an OCR engine compiled to JavaScript. Running locally avoids uploading every image to a server, which matters for privacy and for latency.

The engine returns recognized words and their coordinates. The extension creates a layer above the image with one positioned element per word or line. The text is transparent, but it sits in the same place as the pixels, so a drag selects the words under the cursor.

Because the layer is real text, other features follow. Copy puts the words on the clipboard. A translation action sends the selected string to a translation service. An edit action hides the original region and draws a replacement.

Detection is the weak point. OCR on low-resolution or stylized text produces garbage, so the extension scores confidence and only builds overlays where the result is plausible. Images without text get no layer.

## Build something similar

Take one screenshot with clear text. Run any OCR engine over it and print each word with its bounding box.

Draw absolutely positioned spans over the image using those boxes, with transparent color. Select them with the mouse. If selection lands on the right words, the core mechanism works.

Then handle failure. Rotate the image, blur it, and use a decorative font. Decide what confidence threshold means "no text here" rather than producing nonsense.

## Sources

HackMIT origin is linked in the evidence field.
