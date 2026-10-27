const pending={es:'EXTRACCIÓN PENDIENTE DE COTEJO · NO ES UNA CITA VALIDADA',en:'UNREVIEWED EXTRACTION · NOT A VALIDATED QUOTE',zh:'提取文本尚未核对 · 非已验证引文',pt:'EXTRAÇÃO PENDENTE DE REVISÃO · CITAÇÃO NÃO VALIDADA',fr:'EXTRACTION NON VÉRIFIÉE · CITATION NON VALIDÉE'};
const ready={es:'Escribe una palabra o frase para buscar en la biblioteca.',en:'Enter a word or phrase to search the library.',zh:'请输入字词以搜索资料库。',pt:'Digite uma palavra ou frase para pesquisar.',fr:'Saisissez un mot ou une expression à rechercher.'};
for(const lang of Object.keys(translations))translations[lang].ready=ready[lang];
const states={es:{loading:'Cargando la biblioteca fija de 72 PDF…',ready:'Biblioteca fija: 72 PDF. Los textos extraídos siguen pendientes de cotejo.',unavailable:'La biblioteca de 72 PDF todavía no está habilitada en este despliegue. La aplicación local conserva la biblioteca completa.',error:'No se pudo cargar la biblioteca. Reintenta recargando la página.'},en:{loading:'Loading the fixed 72-PDF library…',ready:'Fixed library: 72 PDFs. Extracted text awaits review.',unavailable:'The 72-PDF library is not yet enabled on this deployment. The local application retains the full library.',error:'The library could not be loaded. Reload to retry.'},zh:{loading:'正在加载72份PDF资料库…',ready:'固定资料库：72份PDF。提取文本尚未核对。',unavailable:'此部署尚未启用72份PDF资料库。本地应用保留完整资料库。',error:'资料库加载失败，请刷新重试。'},pt:{loading:'Carregando a biblioteca fixa de 72 PDFs…',ready:'Biblioteca fixa: 72 PDFs. Texto extraído pendente de revisão.',unavailable:'A biblioteca ainda não está habilitada neste site. O aplicativo local mantém os 72 PDFs.',error:'Não foi possível carregar a biblioteca. Recarregue para tentar novamente.'},fr:{loading:'Chargement de la bibliothèque fixe de 72 PDF…',ready:'Bibliothèque fixe : 72 PDF. Le texte extrait reste à vérifier.',unavailable:'La bibliothèque n’est pas encore activée sur ce site. L’application locale conserve les 72 PDF.',error:'Impossible de charger la bibliothèque. Rechargez la page.'}};
for(const lang of Object.keys(translations))translations[lang].empty=states[lang].unavailable;
let loadState='loading';
const originalLocalize=localize;
function showState(){$('#library-state').textContent=states[$('#locale').value][loadState]}
$('#locale').onchange=()=>{originalLocalize();showState()};
const searchButton=document.querySelector('#search button');
searchButton.disabled=true;
function safeCatalog(c){
  return c?.version===1 &&
  Array.isArray(c.documents) &&
  c.documents.length>=1 &&
  c.documents.every(d=>
    /^[a-f0-9]{64}$/.test(d.sha256) &&
    typeof d.title==='string' &&
    ['es','en','zh','pt','fr'].includes(d.language) &&
    typeof d.reviewed==='boolean' &&
    d.author==='Li Hongzhi' &&
    Array.isArray(d.pages) &&
    d.pages.every(p=>Number.isInteger(p.pdfPage)&&p.pdfPage>0&&typeof p.text==='string') &&
    typeof d.sourceUrl==='string'
  );
}
localize();
showState();
fetch('/library/status.json').then(async r=>{
  if(!r.ok)throw Error('status');
  const status=await r.json();
  if(!status.available){loadState='unavailable';return;}
  const response=await fetch('/library/catalog.json');
  if(!response.ok)throw Error('catalog');
  const c=await response.json();
  if(!safeCatalog(c))throw Error('invalid catalog');
  catalog=c;
  for(const title of new Set(c.documents.map(d=>d.title))) $('#work').add(new Option(title,title));
  loadState='ready';
  searchButton.disabled=false;
  render();
}).catch(()=>{loadState='error';}).finally(showState);
