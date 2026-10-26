# FaStudy

Aplicación independiente y de código abierto para consultar una **biblioteca fija de 72 PDF** de libros y conferencias de Li Hongzhi. No afirma afiliación oficial. Los visitantes no tienen que subir archivos.

## Estado real

- Interfaz en español, inglés, chino, portugués y francés.
- Búsqueda literal; fragmentos con coincidencias resaltadas, contexto completo, copia y enlace a página PDF.
- Consulta local de los mismos 72 documentos; la aplicación no incorpora textos inventados ni un corpus de ejemplo como sustituto.
- Código listo para GitHub y alojamiento estático en Vercel.
- El build público NO incluye PDF ni textos: muestra explícitamente que la biblioteca no está habilitada. No simula una búsqueda sin resultados cuando falta el corpus.
- La publicación compartida de los textos queda pendiente de acreditar su autorización. Descargar gratuitamente no determina el alcance del permiso de reproducción. El índice de origen es https://es.falundafa.org/falun-dafa-books.html .

## Ejecutar con la biblioteca local

Requisitos: Python 3.10+ y una copia de `FaStudy-biblioteca` preparada en el proyecto original. Contiene `pdf/`, `catalogos/` y `respaldo-verificado.json`. Mantenerla FUERA del repositorio. Cada catálogo corresponde al SHA-256 del PDF.

```
python scripts/serve-local.py --library "ruta/a/FaStudy-biblioteca"
```

Abrir http://127.0.0.1:4175 . El servidor escucha exclusivamente en el equipo local y verifica los hashes de los 72 PDF antes de arrancar. No requiere instalar bibliotecas ni subir archivos. Los enlaces conservan `#page=N`; el visor PDF del navegador debe admitirlo (Chrome/Edge). Si el navegador integrado no representa PDF, usar Chrome/Edge o descargar el original.

## Build y Vercel

Node 22 o superior. No hay dependencias npm ni claves de API.

```
npm run check
npm test
npm run build
```

En Vercel: importar el repositorio, Framework Preset «Other», Build Command `npm run build`, Output Directory `dist`, Install Command vacío o `npm install`. `vercel.json` declara la configuración. Vercel ejecutará el build en un checkout limpio. Una carpeta `dist` preexistente con contenido causa un fallo intencionado para no volver a publicar restos de corpus.

## Arquitectura

`web/`: interfaz estática sin analítica ni servicios externos. Busca el catálogo fijo en `/library/catalog.json` solo si `/library/status.json` declara su disponibilidad.

`scripts/serve-local.py`: conecta el mismo código con la biblioteca privada local; sirve únicamente archivos de la aplicación y PDF registrados por hash. No expone un listado de carpetas ni rutas arbitrarias.

`scripts/build.mjs`: produce un despliegue sin corpus. El estado «no habilitado» es distinto de «cero coincidencias».

Para una futura biblioteca compartida autorizada, el administrador deberá publicar estos mismos 72 PDF bajo `/library/pdf/<sha256>.pdf`, el catálogo versionado bajo `/library/catalog.json` y, al final, `status.json` con `available:true`. El catálogo debe conservar `reviewed:false` hasta completar el cotejo: el permiso de publicación y la revisión del texto son estados distintos. No basta con activar `available:true`: deben existir todos los documentos, pasar validaciones y revisarse los controles de acceso. La distribución del corpus NO está implementada en el build actual.

## Fidelidad y límites

Los textos se extraen por página. Las citas conservan la cadena extraída, con elipses visibles para cortes y resaltado que no altera el texto. La extracción automática aún no es una cita validada: comparar contra el PDF. Las páginas vacías se omiten de búsqueda, manteniendo sus índices originales. Los títulos son provisionales cuando proceden del nombre de archivo. Fechas, conferencias y páginas impresas desconocidas se muestran como no disponibles.

La interfaz es multilingüe; esto no implica que existan versiones de los 72 PDF en esos idiomas. El corpus inicial está etiquetado provisionalmente como español. No hay traducción automática, búsqueda semántica, generación de resúmenes ni respuestas doctrinales.

## Contribuir

Abrir cambios pequeños con explicación y comprobaciones. No adjuntar PDF, textos extraídos, permisos confidenciales, credenciales ni rutas personales a commits, incidencias o capturas públicas. Los datos locales y salidas están excluidos por `.gitignore`; aun así revisar `git diff --cached` antes de subir cambios.

MIT cubre solo el código. Los libros, conferencias y traducciones conservan sus derechos. El proyecto no garantiza alojamiento gratuito permanente ni cubre dominios o tráfico fuera de cuotas.
