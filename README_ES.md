# Boletín Multilingüe de Artículos Diarios de HuggingFace

<div align="center">
  <a href="https://internlm.org/">
    <img src="https://internlm.org/assets/logo-a0611363.svg" alt="InternLM" height="80"/>
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://huggingface.co/">
    <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="HuggingFace" height="80"/>
  </a>
</div>

<p align="center">
  <em>Traduciendo artículos diarios de HuggingFace con InternLM</em>
</p>

<div align="center">

[English](README.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md)

</div>

---

Este proyecto descarga y procesa automáticamente los datos de artículos diarios de HuggingFace y los traduce a varios idiomas utilizando el modelo de lenguaje InternLM. El proyecto se ejecuta automáticamente todos los días para garantizar la obtención y traducción oportuna de los últimos artículos.

## Modelo Utilizado

- **Modelo de Traducción**: [InternLM-3](https://internlm.org/)
  - Desarrollador: Laboratorio de IA de Shanghai
  - Versión: internlm3-latest
  - Características:
    - Potente capacidad de traducción multilingüe
    - Comprensión y traducción precisa de textos académicos
    - Traducción en tiempo real a través de API

## Características

- Descarga automática de datos de artículos diarios de HuggingFace
- Soporte para descargar datos históricos de fechas específicas
- Uso de la hora de Beijing como zona horaria predeterminada
- Registro completo de actividades
- Almacenamiento de metadatos de artículos en formato JSON
- Traducción de artículos en inglés a varios idiomas usando InternLM-3:
  - Japonés
  - Coreano
  - Español
  - Francés
- Flujo de trabajo automatizado:
  - Descarga automática diaria de los últimos artículos
  - Traducción automática multilingüe
  - Actualización automática del repositorio

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/yourusername/hf-daily-paper-newsletter-multilingual.git
cd hf-daily-paper-newsletter-multilingual
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Ejecución Manual

#### Descargar artículos del día actual

```bash
python download_papers.py
```

#### Descargar artículos de una fecha específica

```bash
python download_papers.py --date 2024-03-20
```

#### Traducir artículos

Primero obtener una clave API de InternLM y luego ejecutar:

```bash
python translate_papers.py --date 2024-03-20 --api_key your_api_key_here
```

### Ejecución Automática

El proyecto está configurado con dos flujos de trabajo de GitHub Actions:

1. `daily-paper-download.yml`: Descarga automática de los últimos artículos a las 9:00 hora de Beijing
2. `daily-paper-translate.yml`: Traducción automática después de la descarga

Para habilitar la traducción automática, se debe configurar `INTERNLM_API_KEY` en los Secrets del repositorio.

## Almacenamiento de Datos

- Los datos originales de los artículos en inglés se almacenan en el directorio `Paper_metadata_download`
- Los artículos traducidos se almacenan en el directorio `Translated_papers`, organizados por código de idioma:
  - ja/: Traducciones al japonés
  - ko/: Traducciones al coreano
  - es/: Traducciones al español
  - fr/: Traducciones al francés
- Todos los archivos se guardan en formato JSON con nombres en formato `YYYY-MM-DD.json`

## Estados de Retorno

- Éxito: código de salida 0
- Error: código de salida 1
- Sin datos: código de salida 0 (con advertencia en el registro)

## Agradecimientos

- [InternLM](https://internlm.org/) - Por proporcionar capacidades de traducción potentes
- [HuggingFace](https://huggingface.co/) - Por proporcionar datos de artículos diarios 