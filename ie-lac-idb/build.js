const pptxgen = require("pptxgenjs");
const wb = require("./wb.json");

const THEME = { name:"Eight Patents LAC", headFontFace:"Cambria", bodyFontFace:"Calibri",
  colors:{ dk1:"11182B", lt1:"FFFFFF", dk2:"2A3550", lt2:"F4F2EE",
    accent1:"C25E3A", accent2:"1F6F6B", accent3:"D9A441", accent4:"6E7B99",
    accent5:"8C3B2E", accent6:"A8B3C7", hlink:"1F6F6B", folHlink:"6E7B99" } };
const INK="11182B", PAPER="FFFFFF", WARM="F4F2EE", TERRA="C25E3A", TEAL="1F6F6B",
      OCHRE="D9A441", SLATE="6E7B99", MUTED="5A6478", LINE="D8D3CC";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";       // 13.3 x 7.5
pres.theme  = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Group 1, IE University";
pres.title  = "Eight Patents - LAC for the IDB";

const FIRM = "[FIRM: Deloitte / EY / KPMG / PwC]";
const SRC = (t)=>({ text:t, options:{ fontSize:9, color:MUTED, italic:true } });

/* ---------------- layouts ---------------- */
pres.defineSlideMaster({ title:"DARK", background:{ color:INK }, objects:[
  { text:{ text:"", options:{ placeholder:"eyebrow", x:0.9, y:0.75, w:11.5, h:0.3, fontSize:11, color:OCHRE, charSpacing:2, bold:true, margin:0 } } },
  { text:{ text:"", options:{ placeholder:"title", x:0.9, y:1.3, w:11.5, h:2.4, fontSize:44, bold:true, color:PAPER, fontFace:"Cambria", margin:0 } } },
  { text:{ text:"", options:{ placeholder:"body", x:0.9, y:3.9, w:11.5, h:2.4, fontSize:16, color:"C8CEDC", margin:0 } } },
]});

pres.defineSlideMaster({ title:"LIGHT", background:{ color:PAPER }, objects:[
  { text:{ text:"", options:{ placeholder:"eyebrow", x:0.9, y:0.55, w:11.5, h:0.3, fontSize:11, color:TERRA, charSpacing:2, bold:true, margin:0 } } },
  { text:{ text:"", options:{ placeholder:"title", x:0.9, y:0.95, w:7.1, h:1.5, fontSize:34, bold:true, color:INK, fontFace:"Cambria", margin:0 } } },
  { text:{ text:"", options:{ placeholder:"body", x:0.9, y:2.55, w:4.3, h:3.4, fontSize:14, color:MUTED, margin:0 } } },
  { text:{ text:"", options:{ placeholder:"source", x:0.9, y:6.85, w:11.5, h:0.3, fontSize:9, color:MUTED, italic:true, margin:0 } } },
  { text:{ text:"Group 1 · IE University · for the Inter-American Development Bank", options:{ x:0.9, y:6.55, w:8, h:0.25, fontSize:9, color:"A9A399", margin:0 } } },
  { text:{ text:"", options:{ placeholder:"chart", x:5.6, y:1.9, w:6.8, h:4.3, color:MUTED } } },
]});

pres.defineSlideMaster({ title:"WARM", background:{ color:WARM }, objects:[
  { text:{ text:"", options:{ placeholder:"eyebrow", x:0.9, y:0.55, w:11.5, h:0.3, fontSize:11, color:TERRA, charSpacing:2, bold:true, margin:0 } } },
  { text:{ text:"", options:{ placeholder:"title", x:0.9, y:0.95, w:8.5, h:1.5, fontSize:34, bold:true, color:INK, fontFace:"Cambria", margin:0 } } },
  { text:{ text:"", options:{ placeholder:"source", x:0.9, y:6.85, w:11.5, h:0.3, fontSize:9, color:MUTED, italic:true, margin:0 } } },
]});

/* ---------------- helpers ---------------- */
function stat(s,{x,y,n,label,color=TERRA,size=54,w=3.4}){
  s.addText(n,{ x, y, w, h:0.95, fontSize:size, bold:true, color, fontFace:"Cambria", isTextBox:true, margin:0, objectName:`stat-${n}` });
  s.addText(label,{ x, y:y+0.95, w, h:0.75, fontSize:11, color:MUTED, isTextBox:true, margin:0 });
}
function aside(s,t,{x=5.6,y=6.15,w=6.8}={}){
  s.addText(t,{ x,y,w,h:0.35, fontSize:11, italic:true, color:SLATE, isTextBox:true, margin:0 });
}
function card(s,{x,y,w,h,title,text,num,accent=TERRA}){
  s.addShape(pres.ShapeType.roundRect,{ x,y,w,h, fill:{color:PAPER}, line:{color:LINE,width:1}, rectRadius:0.06,
    shadow:{ type:"outer", color:"000000", opacity:0.07, blur:8, offset:2, angle:90 }, objectName:`card-${title}` });
  if(num) s.addText(num,{ x:x+0.3, y:y+0.22, w:0.9, h:0.5, fontSize:22, bold:true, color:accent, fontFace:"Cambria", isTextBox:true, margin:0 });
  s.addText(title,{ x:x+0.3, y:y+0.72, w:w-0.6, h:0.45, fontSize:15, bold:true, color:INK, isTextBox:true, margin:0 });
  s.addText(text,{ x:x+0.3, y:y+1.18, w:w-0.6, h:h-1.45, fontSize:12, color:MUTED, isTextBox:true, margin:0 });
}
const axis = { catAxisLabelColor:MUTED, valAxisLabelColor:MUTED, catAxisLabelFontSize:10, valAxisLabelFontSize:10,
  catAxisLabelFontFace:"+mn-lt", valAxisLabelFontFace:"+mn-lt", valGridLine:{ color:"E8E4DE", size:1 },
  catGridLine:{ style:"none" }, showLegend:false, chartColors:[TERRA], border:{pt:0,color:"FFFFFF"} };

const yrs=(o,a,b)=>Object.keys(o).map(Number).filter(y=>y>=a&&y<=b).sort((x,y)=>x-y);

/* ======================= 1 TITLE ======================= */
pres.addSection({ title:"Title" });
let s = pres.addSlide({ masterName:"DARK", sectionTitle:"Title" });
s.addText("FOR THE INTER-AMERICAN DEVELOPMENT BANK",{ placeholder:"eyebrow" });
s.addText([{text:"Eight\npatents",options:{color:PAPER}}],{ placeholder:"title" });
s.addText("What Mexico and Central America stopped buying, and what it cost them.\n\nA whole subregion's output of new ideas, 2024.",{ placeholder:"body" });
s.addText([
  {text:"Group 1",options:{bold:true,color:PAPER}},{text:"  ·  ",options:{color:SLATE}},
  {text:"Mexico & Central America",options:{color:"C8CEDC"}},{text:"  ·  ",options:{color:SLATE}},
  {text:"Inter-American Development Bank",options:{color:"C8CEDC"}},{text:"  ·  ",options:{color:SLATE}},
  {text:FIRM,options:{color:OCHRE,bold:true}},
],{ x:0.9, y:6.5, w:11.5, h:0.4, fontSize:12, isTextBox:true, margin:0 });
s.addShape(pres.ShapeType.rect,{ x:0.9, y:6.35, w:1.1, h:0.03, fill:{color:TERRA} });
s.addNotes("Group 1. Mexico and Central America, for the IDB. The question the Bank asked is why growth has been so disappointing. Our answer starts with one number.");

/* ======================= 2-3 EXECUTIVE SUMMARY ======================= */
pres.addSection({ title:"Executive summary" });
s = pres.addSlide({ masterName:"WARM", sectionTitle:"Executive summary" });
s.addText("EXECUTIVE SUMMARY · THE FINDING",{ placeholder:"eyebrow" });
s.addText("Growth did not fail. A purchase was never made",{ placeholder:"title" });
s.addText("The subregion did not lose a race it was running. It stopped buying the one thing that compounds: the capability to make hard things. Korea bought it from the same starting line in 1980.",
  { x:0.9, y:2.35, w:5.1, h:1.4, fontSize:15, color:MUTED, isTextBox:true, margin:0 });
stat(s,{x:0.9,y:3.9,n:"8",label:"Patents filed by residents of Guatemala, whole country, 2024",w:2.3});
stat(s,{x:3.4,y:3.9,n:"1",label:"Researchers in R&D per million people, Guatemala, 2023",w:2.3,color:TERRA});
card(s,{x:6.3,y:2.3,w:6.1,h:1.35,title:"Two reasons, not ten",text:"Capital cities pull in people and money and send little back. Payroll taxes make being visible expensive, so firms stay small.",num:"01"});
card(s,{x:6.3,y:3.8,w:6.1,h:1.35,title:"It has been solved here before",text:"Chile in salmon, Costa Rica in medical devices, Medellin in its hillsides. Each a state doing one narrow thing for a long time.",num:"02"});
card(s,{x:6.3,y:5.3,w:6.1,h:1.0,title:"One ask, this year",text:"Fund a capability agency in one country. The factories are choosing where to land now.",num:"03"});
s.addText("Patents IP.PAT.RESD; researchers SP.POP.SCIE.RD.P6 · World Bank WDI · retrieved 20 Oct 2026",{ placeholder:"source" });
s.addNotes("The finding in one line: this is not a mystery of culture or geography, it is a purchase nobody made. Two reasons. Three precedents in this region. One ask.");

s = pres.addSlide({ masterName:"WARM", sectionTitle:"Executive summary" });
s.addText("EXECUTIVE SUMMARY · WHAT WE PROPOSE",{ placeholder:"eyebrow" });
s.addText("Three programmes, sequenced for political survival",{ placeholder:"title" });
const progs=[
  ["01","Take the wall down","Pay health and pensions from general tax, not from wages. Years 0 to 2, felt inside one electoral term.",TERRA],
  ["02","Learn new industries","A capability agency that learns an industry, then hands it to firms. Years 2 to 5, the window is open now.",TEAL],
  ["03","Reach the towns outside","Roads and connectivity to the periphery the capital wrote off. Years 5 to 10, needs the tax base first.",OCHRE]];
progs.forEach((p,i)=>card(s,{x:0.9+i*3.95,y:2.4,w:3.6,h:2.5,num:p[0],title:p[1],text:p[2],accent:p[3]}));
s.addText("We are not promising a growth number",{ x:0.9, y:5.25, w:6.5, h:0.4, fontSize:17, bold:true, color:INK, fontFace:"Cambria", isTextBox:true, margin:0 });
s.addText("No comparable subregion has run this package before. We commit to three published counts instead: patents filed, how far the poorest region trails, and how many workers are on the books.",
  { x:0.9, y:5.7, w:11.5, h:0.9, fontSize:13, color:MUTED, isTextBox:true, margin:0 });
s.addText("Programme design original · precedents named on slides 13 to 16 · costings to be built with IDB project data",{ placeholder:"source" });
s.addNotes("Order is chosen for political survival, not analytical elegance. The cheap visible one goes first because it buys room for the next.");

/* ======================= 4-6 REGIONAL CONTEXT ======================= */
pres.addSection({ title:"Regional context" });
s = pres.addSlide({ masterName:"LIGHT", sectionTitle:"Regional context" });
s.addText("REGIONAL CONTEXT · INCOME",{ placeholder:"eyebrow" });
s.addText("Eight countries, a sixfold spread",{ placeholder:"title" });
s.addText("GDP per person, constant 2015 US dollars, 2025. Panama and Costa Rica sit in a different economy from Honduras and Nicaragua, inside one subregion the Bank treats as one client.",
  { placeholder:"body" });
s.addChart(pres.ChartType.bar,[{ name:"GDP per person", labels:["Panama","Costa Rica","Mexico","Belize","El Salvador","Guatemala","Honduras","Nicaragua"],
  values:[17650,15669,10257,6374,4735,4688,2628,2372] }],
  { placeholder:"chart", ...axis, barDir:"bar", showValue:true, dataLabelPosition:"outEnd", dataLabelColor:MUTED,
    dataLabelFontSize:10, dataLabelFontFace:"+mn-lt", dataLabelFormatCode:'$#,##0', valAxisHidden:true, barGapWidthPct:45 });
s.addText("GDP per capita, constant 2015 US$ · World Bank WDI, NY.GDP.PCAP.KD · retrieved 20 Oct 2026",{ placeholder:"source" });
s.addNotes("One subregion, but not one economy. Panama is seven times Nicaragua.");

s = pres.addSlide({ masterName:"LIGHT", sectionTitle:"Regional context" });
s.addText("REGIONAL CONTEXT · GROWTH AND POVERTY",{ placeholder:"eyebrow" });
s.addText("The largest economy has stopped moving",{ placeholder:"title" });
s.addText("Real GDP growth, 2025. Mexico is 40 percent of the subregion's output and grew at 0.6 percent while its smaller neighbours ran between 2.7 and 4.9.",{ placeholder:"body" });
stat(s,{x:0.9,y:4.6,n:"0.6%",label:"Mexico real GDP growth, 2025",w:2.3,size:40});
stat(s,{x:3.4,y:4.6,n:"60.1%",label:"Honduras poverty headcount, national line, 2025",w:2.3,size:40,color:TEAL});
s.addChart(pres.ChartType.bar,[{ name:"Real GDP growth 2025", labels:["Nicaragua","Costa Rica","Panama","Guatemala","El Salvador","Honduras","Belize","Mexico"],
  values:[4.9,4.6,4.4,4.3,3.9,3.8,2.7,0.6] }],
  { placeholder:"chart", ...axis, barDir:"bar", showValue:true, dataLabelPosition:"outEnd", dataLabelColor:MUTED,
    dataLabelFontSize:10, dataLabelFontFace:"+mn-lt", dataLabelFormatCode:'0.0"%"', valAxisHidden:true, barGapWidthPct:45 });
s.addText("Real GDP growth NY.GDP.MKTP.KD.ZG; poverty SI.POV.NAHC · World Bank WDI · retrieved 20 Oct 2026 · Mexico output share UNSURE, to be verified",{ placeholder:"source" });
s.addNotes("Mexico at 0.6 percent is the anomaly. The convergence story people expect from NAFTA is not in the data.");

s = pres.addSlide({ masterName:"WARM", sectionTitle:"Regional context" });
s.addText("REGIONAL CONTEXT · THE SIGNAL",{ placeholder:"eyebrow" });
s.addText("Its inventors filed eight patents all year",{ placeholder:"title" });
s.addText("Not eight thousand. Eight.",{ x:0.9, y:2.3, w:5.3, h:0.5, fontSize:20, italic:true, color:TERRA, isTextBox:true, margin:0 });
s.addText("Guatemala, 2024. Population 18.4 million.",{ x:0.9, y:2.85, w:5.3, h:0.4, fontSize:14, color:MUTED, isTextBox:true, margin:0 });
stat(s,{x:0.9,y:3.5,n:"8",label:"Patent applications, whole country, whole year",w:2.4,size:70});
stat(s,{x:3.6,y:3.5,n:"195,786",label:"Patent applications, South Korea, same year, same definition",w:2.8,size:36,color:TEAL});
const perM=[["Guatemala",0.4],["Costa Rica",2.9],["Mexico",9.0],["Chile",19.7],["Brazil",27.1],["South Korea",3783]];
s.addText("Patents per million people, 2024",{ x:6.9, y:2.3, w:5.5, h:0.35, fontSize:12, bold:true, color:INK, isTextBox:true, margin:0 });
perM.forEach((r,i)=>{
  const y=2.75+i*0.62;
  s.addText(r[0],{ x:6.9, y, w:2.2, h:0.4, fontSize:13, color:INK, isTextBox:true, margin:0 });
  s.addText(String(r[1]),{ x:9.2, y, w:1.1, h:0.4, fontSize:13, bold:true, color:(i===5?TEAL:TERRA), align:"right", isTextBox:true, margin:0 });
  if(i<5) s.addShape(pres.ShapeType.rect,{ x:10.5, y:y+0.13, w:Math.max(0.03,(r[1]/3783)*1.8), h:0.14, fill:{color:TERRA} });
  else s.addShape(pres.ShapeType.rect,{ x:10.5, y:y+0.13, w:1.8, h:0.14, fill:{color:TEAL} });
});
aside(s,"420x Korea's filings per person against Mexico's. Against Guatemala, 8,704x.",{x:6.9,y:6.1,w:5.5});
s.addText("Patents by residents / population, 2024 · World Bank WDI, IP.PAT.RESD and SP.POP.TOTL · retrieved 20 Oct 2026",{ placeholder:"source" });
s.addNotes("This is the signal. One number that tells you the capability is not there.");

/* ======================= 7-11 DIAGNOSTIC ======================= */
pres.addSection({ title:"Diagnostic" });
s = pres.addSlide({ masterName:"LIGHT", sectionTitle:"Diagnostic" });
s.addText("DIAGNOSTIC · THE REVERSAL",{ placeholder:"eyebrow" });
s.addText("Korea was standing right here",{ placeholder:"title" });
s.addText("In 1980 Mexico and Korea filed almost the same number of patents. Korea's entire lead was 1.8 times. This gap is not ancient. It was built inside one career.",{ placeholder:"body" });
stat(s,{x:0.9,y:4.8,n:"704",label:"Mexico, patents filed, 1980",w:2.3,size:40});
stat(s,{x:3.4,y:4.8,n:"1,241",label:"Korea, patents filed, 1980",w:2.3,size:40,color:TEAL});
const py=yrs(wb.patents["Korea, Rep."],1980,2024);
s.addChart(pres.ChartType.line,[
  { name:"Korea", labels:py.map(String), values:py.map(y=>wb.patents["Korea, Rep."][y]??null) },
  { name:"Mexico", labels:py.map(String), values:py.map(y=>wb.patents["Mexico"][y]??null) },
  { name:"Brazil", labels:py.map(String), values:py.map(y=>wb.patents["Brazil"][y]??null) },
],{ placeholder:"chart", ...axis, chartColors:[TEAL,TERRA,SLATE], showLegend:true, legendPos:"b", legendColor:MUTED,
    legendFontSize:10, legendFontFace:"+mn-lt", lineSize:2, lineSmooth:false, showMarker:false, catAxisLabelFrequency:5 });
s.addText("Patent applications by residents, 1980 to 2024 · World Bank WDI, IP.PAT.RESD · retrieved 20 Oct 2026",{ placeholder:"source" });
s.addNotes("Same starting line. Forty-four years. Korea multiplied its filings by 158; Mexico by 1.7.");

s = pres.addSlide({ masterName:"LIGHT", sectionTitle:"Diagnostic" });
s.addText("DIAGNOSTIC · THE BILL",{ placeholder:"eyebrow" });
s.addText("Sixty-four years later, here is the bill",{ placeholder:"title" });
s.addText("Income per person, constant 2015 US dollars, 1960 to 2024. In 1960 Mexico was four times richer than Korea. The lines cross in 1988 and never cross back.",{ placeholder:"body" });
stat(s,{x:0.9,y:4.8,n:"3.6x",label:"Korea's income per person against Mexico's, 2024",w:2.3,size:40,color:TEAL});
stat(s,{x:3.4,y:4.8,n:"1988",label:"The year the two lines swap",w:2.3,size:40});
const gy=yrs(wb.gdppc["Korea, Rep."],1960,2024);
s.addChart(pres.ChartType.line,[
  { name:"Korea", labels:gy.map(String), values:gy.map(y=>wb.gdppc["Korea, Rep."][y]??null) },
  { name:"Mexico", labels:gy.map(String), values:gy.map(y=>wb.gdppc["Mexico"][y]??null) },
  { name:"Guatemala", labels:gy.map(String), values:gy.map(y=>wb.gdppc["Guatemala"][y]??null) },
],{ placeholder:"chart", ...axis, chartColors:[TEAL,TERRA,OCHRE], showLegend:true, legendPos:"b", legendColor:MUTED,
    legendFontSize:10, legendFontFace:"+mn-lt", lineSize:2, lineSmooth:false, showMarker:false, catAxisLabelFrequency:8,
    valAxisLabelFormatCode:'$#,##0' });
s.addText("GDP per capita, constant 2015 US$ · World Bank WDI, NY.GDP.PCAP.KD · retrieved 20 Oct 2026",{ placeholder:"source" });
s.addNotes("Korea 37,048 dollars. Mexico 10,284. Guatemala 4,564. Real income, not prices.");

s = pres.addSlide({ masterName:"DARK", sectionTitle:"Diagnostic" });
s.addText("DIAGNOSTIC · THE ARGUMENT",{ placeholder:"eyebrow" });
s.addText("This is not a mystery.\nIt is a purchase\nnobody made",{ placeholder:"title" });
s.addText("Knowing how to make hard things is not a national character trait. It is bought, slowly, on purpose.\n\nEverything before this slide was evidence. Everything after it is what to do.",{ placeholder:"body" });
s.addText("Argument, not data · follows from the preceding slides · framing after Hausmann, Rodrik and Velasco, growth diagnostics",
  { x:0.9, y:6.85, w:11.5, h:0.3, fontSize:9, color:SLATE, italic:true, isTextBox:true, margin:0 });
s.addNotes("This is the hinge of the deck. Pause here.");

s = pres.addSlide({ masterName:"WARM", sectionTitle:"Diagnostic" });
s.addText("DIAGNOSTIC · REASON ONE",{ placeholder:"eyebrow" });
s.addText("The big cities took, and sent nothing back",{ placeholder:"title" });
s.addText("People, money and talent flowed in. Jobs and roads never flowed out. Myrdal called it backwash: what happens when growth concentrates instead of spreading.",
  { x:0.9, y:2.4, w:5.0, h:1.3, fontSize:14, color:MUTED, isTextBox:true, margin:0 });
s.addText("Backwash",{ x:0.9, y:3.9, w:5.0, h:0.5, fontSize:26, bold:true, color:TERRA, fontFace:"Cambria", isTextBox:true, margin:0 });
s.addText("Myrdal, 1957",{ x:0.9, y:4.45, w:5.0, h:0.3, fontSize:12, color:MUTED, isTextBox:true, margin:0 });
s.addShape(pres.ShapeType.ellipse,{ x:8.3, y:3.0, w:1.9, h:1.9, fill:{color:TEAL}, objectName:"capital" });
s.addText("Capital",{ x:8.3, y:3.72, w:1.9, h:0.45, fontSize:13, bold:true, color:PAPER, align:"center", isTextBox:true, margin:0 });
[[6.6,2.5],[6.6,3.95],[6.6,5.4],[11.2,2.5],[11.2,3.95],[11.2,5.4]].forEach((p,i)=>{
  s.addShape(pres.ShapeType.ellipse,{ x:p[0], y:p[1], w:0.75, h:0.75, fill:{color:"FFFFFF"}, line:{color:LINE,width:1} });
});
s.addText("Pulled in",{ x:6.3, y:6.3, w:2.2, h:0.3, fontSize:11, bold:true, color:TERRA, isTextBox:true, margin:0 });
s.addText("Given back",{ x:10.9, y:6.3, w:2.2, h:0.3, fontSize:11, bold:true, color:SLATE, isTextBox:true, margin:0 });
[[7.35,2.87],[7.35,4.32],[7.35,5.77]].forEach(p=>s.addShape(pres.ShapeType.rect,{ x:p[0], y:p[1], w:0.95, h:0.12, fill:{color:TERRA} }));
[[10.2,2.87],[10.2,4.32],[10.2,5.77]].forEach(p=>s.addShape(pres.ShapeType.rect,{ x:p[0], y:p[1], w:0.95, h:0.03, fill:{color:SLATE} }));
aside(s,"Economists call this backwash. Everyone else calls it leaving.",{x:0.9,y:5.4,w:5.0});
s.addText("Growth pole theory: Perroux 1955 · Myrdal 1957 · Hirschman 1958 · diagram illustrative, not to scale",{ placeholder:"source" });
s.addNotes("Thick bars in, hairlines out. Concept, not data.");

s = pres.addSlide({ masterName:"WARM", sectionTitle:"Diagnostic" });
s.addText("DIAGNOSTIC · REASON TWO",{ placeholder:"eyebrow" });
s.addText("Hiring someone openly costs extra",{ placeholder:"title" });
s.addText("So firms stay small, stay hidden, and never learn to grow. Payroll taxes buy invisibility.",
  { x:0.9, y:2.4, w:5.0, h:0.9, fontSize:14, color:MUTED, isTextBox:true, margin:0 });
s.addText("Payroll taxes buy\ninvisibility",{ x:0.9, y:3.5, w:5.0, h:1.0, fontSize:24, bold:true, color:TERRA, fontFace:"Cambria", isTextBox:true, margin:0 });
s.addText("Mechanism after Santiago Levy",{ x:0.9, y:4.6, w:5.0, h:0.3, fontSize:12, color:MUTED, isTextBox:true, margin:0 });
s.addShape(pres.ShapeType.rect,{ x:8.6, y:2.3, w:0.02, h:4.0, fill:{color:TERRA}, objectName:"wall" });
s.addText("The moment the state can see the firm",{ x:7.35, y:1.95, w:2.6, h:0.3, fontSize:10, italic:true, color:TERRA, align:"center", isTextBox:true, margin:0 });
[[6.5,3.0],[7.2,3.9],[6.5,4.8],[7.6,5.3]].forEach(p=>s.addShape(pres.ShapeType.ellipse,{ x:p[0], y:p[1], w:0.55, h:0.55, fill:{color:TEAL} }));
[[9.4,3.0],[10.3,3.6],[11.2,4.3],[10.0,5.1]].forEach(p=>s.addShape(pres.ShapeType.ellipse,{ x:p[0], y:p[1], w:0.55, h:0.55, fill:{color:WARM}, line:{color:SLATE,width:1} }));
s.addText("Stays small",{ x:6.3, y:6.0, w:2.2, h:0.3, fontSize:12, bold:true, color:TEAL, isTextBox:true, margin:0 });
s.addText("Never happens",{ x:9.6, y:6.0, w:2.6, h:0.3, fontSize:12, bold:true, color:SLATE, isTextBox:true, margin:0 });
aside(s,"About half the workforce lives to the left of that line, a figure we still have to pull ourselves.",{x:0.9,y:5.2,w:5.2});
s.addText("Mechanism after Santiago Levy · diagram illustrative · exact informality rate UNSURE until pulled from ILOSTAT, see appendix",{ placeholder:"source" });
s.addNotes("Solid circles are the firm today. Hollow is the growth that never comes.");

/* ======================= 12-13 BENCHMARKS ======================= */
pres.addSection({ title:"International benchmarks" });
s = pres.addSlide({ masterName:"LIGHT", sectionTitle:"International benchmarks" });
s.addText("INTERNATIONAL BENCHMARKS · WHAT KOREA ACTUALLY BOUGHT",{ placeholder:"eyebrow" });
s.addText("People whose whole job is to find things out",{ placeholder:"title" });
s.addText("Researchers in R&D per million people. The patent gap is downstream of this one. Korea did not out-think the region, it out-hired it, for forty years.",{ placeholder:"body" });
stat(s,{x:0.9,y:4.8,n:"9,472",label:"Korea, researchers per million, 2023",w:2.3,size:36,color:TEAL});
stat(s,{x:3.4,y:4.8,n:"1",label:"Guatemala, researchers per million, 2023",w:2.3,size:36});
s.addChart(pres.ChartType.bar,[{ name:"Researchers per million", labels:["Korea","Costa Rica","Mexico","Guatemala"], values:[9472,508,438,1] }],
  { placeholder:"chart", ...axis, barDir:"bar", chartColors:[TEAL], showValue:true, dataLabelPosition:"outEnd",
    dataLabelColor:MUTED, dataLabelFontSize:11, dataLabelFontFace:"+mn-lt", dataLabelFormatCode:'#,##0', valAxisHidden:true, barGapWidthPct:50 });
s.addText("Researchers in R&D per million people · World Bank WDI, SP.POP.SCIE.RD.P6 · Korea, Costa Rica, Guatemala 2023; Mexico 2024 · retrieved 20 Oct 2026",{ placeholder:"source" });
s.addNotes("Korea has nine thousand times Guatemala's research workforce per head. That is the purchase.");

s = pres.addSlide({ masterName:"WARM", sectionTitle:"International benchmarks" });
s.addText("INTERNATIONAL BENCHMARKS · THIS REGION",{ placeholder:"eyebrow" });
s.addText("This has already been done. Here. On purpose",{ placeholder:"title" });
s.addText("Three cases from Latin America, each engineered by a state that did one narrow thing for a long time. None of it was luck. All of it was policy.",
  { x:0.9, y:2.35, w:11.5, h:0.6, fontSize:14, color:MUTED, isTextBox:true, margin:0 });
[["Chile","Fundacion Chile","Learned to farm salmon itself, proved it worked, then handed the industry to private firms and stepped back.",TEAL],
 ["Costa Rica","CINDE","Went from bananas to medical devices in one generation by targeting a narrow set of investors and keeping them.",TERRA],
 ["Medellin","Social urbanism","Built cable cars into the hillsides the city had written off. It was never a transport project.",OCHRE]
].forEach((c,i)=>{
  const x=0.9+i*3.95;
  s.addShape(pres.ShapeType.roundRect,{ x, y:3.15, w:3.6, h:2.9, fill:{color:PAPER}, line:{color:LINE,width:1}, rectRadius:0.06,
    shadow:{ type:"outer", color:"000000", opacity:0.07, blur:8, offset:2, angle:90 } });
  s.addText(c[0],{ x:x+0.3, y:3.4, w:3.0, h:0.45, fontSize:19, bold:true, color:c[3], fontFace:"Cambria", isTextBox:true, margin:0 });
  s.addText(c[1],{ x:x+0.3, y:3.88, w:3.0, h:0.35, fontSize:11, bold:true, color:MUTED, charSpacing:1, isTextBox:true, margin:0 });
  s.addText(c[2],{ x:x+0.3, y:4.35, w:3.0, h:1.5, fontSize:12.5, color:MUTED, isTextBox:true, margin:0 });
});
aside(s,"Each one a state doing a narrow thing for longer than one electoral term.",{x:0.9,y:6.2,w:9});
s.addText("Fundacion Chile · CINDE Costa Rica · Medellin social urbanism, from our International Cities session · no figures claimed on this slide",{ placeholder:"source" });
s.addNotes("Deliberately no numbers here. These are existence proofs, not benchmarks to copy line by line.");

/* ======================= 14-18 POLICY ======================= */
pres.addSection({ title:"Policy recommendations" });
const P=[
 { e:"PROGRAMME ONE", t:"Fund a capability agency", lead:"One agency, one country, one industry at a time. It learns the industry itself, de-risks it, then hands it to firms and withdraws.",
   stat:["Years 0-2","Felt inside one electoral term"], prec:"Precedent: Fundacion Chile, CINDE Costa Rica",
   pts:["Pick one tradeable industry with a real window open now","State carries the first-mover risk, not the firms","Hand over on a published date and withdraw","Fund the agency, not the factories"],
   src:"Programme design original · precedents Fundacion Chile and CINDE Costa Rica · costing UNSURE, to be built with IDB project data", acc:TERRA },
 { e:"PROGRAMME TWO", t:"Reach the towns outside", lead:"Perroux's growth pole has five stages. Two of them fail by default, and those are the two the money attaches to.",
   stat:["Years 5-10","Needs the tax base first"], prec:"Case: Medellin cable cars were stage five, not a transport project",
   pts:["Roads and signal reach the towns outside the pole","Local firms learn to supply the centre","Skills spread outward instead of draining in","The last two stages never happen on their own"],
   src:"Perroux's five-stage growth pole process, from our Core-Periphery session · case Medellin · costing UNSURE", acc:OCHRE },
 { e:"PROGRAMME THREE", t:"Take the wall down", lead:"Pay for health and pensions from general tax, not from wages. This costs money before it saves money, and it is the only one that pays back inside one term.",
   stat:["Years 0-2","The only one that pays back fast"], prec:"Mechanism after Santiago Levy · precedents to verify: Brazil SIMPLES, Mexico RIF",
   pts:["Stop taxing the act of being visible","Firms can pass ten employees without hiding","Same firms, wall removed","Say the cost out loud before anyone asks"],
   src:"Mechanism after Santiago Levy · precedents to verify Brazil SIMPLES and Mexico RIF · costing UNSURE", acc:TEAL }];
P.forEach(p=>{
  const sl = pres.addSlide({ masterName:"LIGHT", sectionTitle:"Policy recommendations" });
  sl.addText(p.e,{ placeholder:"eyebrow" });
  sl.addText(p.t,{ placeholder:"title" });
  sl.addText(p.lead,{ placeholder:"body" });
  stat(sl,{x:0.9,y:5.1,n:p.stat[0],label:p.stat[1],w:4.3,size:30,color:p.acc});
  sl.addShape(pres.ShapeType.roundRect,{ x:5.9, y:1.95, w:6.5, h:4.3, fill:{color:WARM}, line:{color:LINE,width:1}, rectRadius:0.06 });
  sl.addText("How it works",{ x:6.25, y:2.2, w:5.8, h:0.35, fontSize:12, bold:true, color:p.acc, charSpacing:1, isTextBox:true, margin:0 });
  sl.addText(p.pts.map((x,i)=>({ text:x, options:{ bullet:true, breakLine:i<p.pts.length-1 } })),
    { x:6.25, y:2.65, w:5.8, h:2.4, fontSize:13, color:INK, paraSpaceAfter:10, isTextBox:true, margin:0 });
  sl.addText(p.prec,{ x:6.25, y:5.5, w:5.8, h:0.55, fontSize:11, italic:true, color:MUTED, isTextBox:true, margin:0 });
  sl.addText(p.src,{ placeholder:"source" });
  sl.addNotes(p.t+". "+p.lead);
});

s = pres.addSlide({ masterName:"WARM", sectionTitle:"Policy recommendations" });
s.addText("POLICY RECOMMENDATIONS · SEQUENCING",{ placeholder:"eyebrow" });
s.addText("Governments last four years. These do not",{ placeholder:"title" });
s.addText("So the order is chosen for political survival, not analytical elegance. Each one buys the political room for the next, which is why the cheap, visible one goes first.",
  { x:0.9, y:2.35, w:11.5, h:0.6, fontSize:14, color:MUTED, isTextBox:true, margin:0 });
const bands=[["Take the wall down",0,2,TEAL],["Learn new industries",2,5,TERRA],["Reach the towns outside",5,10,OCHRE]];
const X0=0.9, XW=11.5;
bands.forEach((b,i)=>{
  const y=3.5+i*0.95;
  s.addShape(pres.ShapeType.roundRect,{ x:X0+(b[1]/10)*XW, y, w:((b[2]-b[1])/10)*XW, h:0.6, fill:{color:b[3]}, rectRadius:0.05 });
  s.addText(b[0],{ x:X0+(b[1]/10)*XW+0.18, y:y+0.08, w:((b[2]-b[1])/10)*XW-0.36, h:0.45, fontSize:13, bold:true, color:PAPER, isTextBox:true, margin:0 });
  s.addText(`Years ${b[1]} to ${b[2]}`,{ x:X0+(b[1]/10)*XW, y:y+0.62, w:3, h:0.28, fontSize:10, color:MUTED, isTextBox:true, margin:0 });
});
[0,2,5,10].forEach(t=>s.addText("Year "+t,{ x:X0+(t/10)*XW-0.3, y:6.25, w:0.9, h:0.3, fontSize:10, color:MUTED, align:"center", isTextBox:true, margin:0 }));
s.addShape(pres.ShapeType.rect,{ x:X0, y:6.18, w:XW, h:0.015, fill:{color:LINE} });
aside(s,"A plan that ignores the electoral calendar never happens.",{x:0.9,y:6.55,w:8});
s.addText("Timeline illustrative · costings UNSURE, to be built from IDB project data and national budgets",{ placeholder:"source" });
s.addNotes("Bands are sequencing, not costings. Each begins once the one before has shown something.");

s = pres.addSlide({ masterName:"LIGHT", sectionTitle:"Policy recommendations" });
s.addText("POLICY RECOMMENDATIONS · ACCOUNTABILITY",{ placeholder:"eyebrow" });
s.addText("Three counts, published every year",{ placeholder:"title" });
s.addText("If the IDB funds this, these are the numbers that go on the record. We are not promising a growth number: no comparable subregion has run this package before.",{ placeholder:"body" });
[["How many patents we file","Benchmarked against Chile and Brazil, not against Korea",TERRA],
 ["How far the poorest region trails","Income per person, richest region against poorest",TEAL],
 ["How many workers are on the books","And how many firms pass ten employees",OCHRE]
].forEach((c,i)=>{
  const y=2.0+i*1.45;
  s.addShape(pres.ShapeType.roundRect,{ x:5.9, y, w:6.5, h:1.2, fill:{color:WARM}, line:{color:LINE,width:1}, rectRadius:0.06 });
  s.addShape(pres.ShapeType.ellipse,{ x:6.2, y:y+0.35, w:0.5, h:0.5, fill:{color:c[2]} });
  s.addText(String(i+1),{ x:6.2, y:y+0.42, w:0.5, h:0.36, fontSize:14, bold:true, color:PAPER, align:"center", isTextBox:true, margin:0 });
  s.addText(c[0],{ x:6.95, y:y+0.26, w:5.2, h:0.4, fontSize:14, bold:true, color:INK, isTextBox:true, margin:0 });
  s.addText(c[1],{ x:6.95, y:y+0.66, w:5.2, h:0.4, fontSize:11.5, color:MUTED, isTextBox:true, margin:0 });
});
aside(s,"A number we cannot defend is worth less than an honest blank.",{x:0.9,y:5.6,w:4.6});
s.addText("Baselines to be set from World Bank, ILOSTAT and national accounts · target levels UNSURE",{ placeholder:"source" });
s.addNotes("We refuse to put a GDP number on this. That refusal is the point.");

/* ======================= 19-20 CONCLUSION ======================= */
pres.addSection({ title:"Conclusion and next steps" });
s = pres.addSlide({ masterName:"WARM", sectionTitle:"Conclusion and next steps" });
s.addText("CONCLUSION · WHAT WE ARE ASKING THE BANK TO DO",{ placeholder:"eyebrow" });
s.addText("Priority actions for the client",{ placeholder:"title" });
[["01","Fund one capability agency","One country, this financial year. Not a regional facility, not a study.",TERRA],
 ["02","Commission the costings","Three programmes, built from IDB project data and national budgets. None are costed yet and we have said so throughout.",TEAL],
 ["03","Set the three baselines","Patents, regional income spread, workers on the books. From World Bank, ILOSTAT and national accounts.",OCHRE],
 ["04","Pull the informality number","From ILOSTAT, for each of the eight countries. It is the one figure our diagnostic leans on and has not yet verified.",SLATE]
].forEach((c,i)=>{
  const x=0.9+(i%2)*5.95, y=2.4+Math.floor(i/2)*2.05;
  s.addShape(pres.ShapeType.roundRect,{ x, y, w:5.6, h:1.8, fill:{color:PAPER}, line:{color:LINE,width:1}, rectRadius:0.06,
    shadow:{ type:"outer", color:"000000", opacity:0.06, blur:7, offset:2, angle:90 } });
  s.addText(c[0],{ x:x+0.3, y:y+0.22, w:0.8, h:0.42, fontSize:18, bold:true, color:c[3], fontFace:"Cambria", isTextBox:true, margin:0 });
  s.addText(c[1],{ x:x+0.3, y:y+0.66, w:5.0, h:0.4, fontSize:15, bold:true, color:INK, isTextBox:true, margin:0 });
  s.addText(c[2],{ x:x+0.3, y:y+1.06, w:5.0, h:0.6, fontSize:12, color:MUTED, isTextBox:true, margin:0 });
});
s.addText("Sixty-four years is long enough to wait for the second attempt",{ x:0.9, y:6.5, w:11.5, h:0.35, fontSize:13, italic:true, color:TERRA, isTextBox:true, margin:0 });
s.addText("Group 1 · IE University · Economics for Public Sector",{ placeholder:"source" });
s.addNotes("Four actions. The first is the ask; the other three are the work that makes it real.");

s = pres.addSlide({ masterName:"DARK", sectionTitle:"Conclusion and next steps" });
s.addText("ONE ASK",{ placeholder:"eyebrow" });
s.addText("Fund the capability\nagency. In one country.\nThis year",{ placeholder:"title" });
s.addText("The factories are choosing where to land right now. In five years this ask is worth less.",{ placeholder:"body" });
s.addShape(pres.ShapeType.rect,{ x:0.9, y:6.3, w:1.1, h:0.03, fill:{color:TERRA} });
s.addText("Group 1  ·  Mexico & Central America  ·  Inter-American Development Bank  ·  "+FIRM,
  { x:0.9, y:6.5, w:11.5, h:0.35, fontSize:11, color:SLATE, isTextBox:true, margin:0 });
s.addNotes("Close here. Then questions.");

/* ======================= APPENDIX ======================= */
pres.addSection({ title:"Appendix" });
s = pres.addSlide({ masterName:"LIGHT", sectionTitle:"Appendix" });
s.addText("APPENDIX · BEHIND THE STORY",{ placeholder:"eyebrow" });
s.addText("What is solid, what is not, and how this was made",{ placeholder:"title" });
[["Verified, with code","All figures pulled from World Bank WDI on 20 Oct 2026: patents IP.PAT.RESD, population SP.POP.TOTL, researchers SP.POP.SCIE.RD.P6, income NY.GDP.PCAP.KD, growth NY.GDP.MKTP.KD.ZG, poverty SI.POV.NAHC. Guatemala 8 patents. Korea 195,786. Every ratio recomputed from the raw series, not quoted.",TEAL],
 ["Unsure, not pulled yet","Informality rate. Chiapas income and poverty. Urban primacy share. Mexico's share of subregional output. Every costing in the three programmes. None appears as a number on any slide. Sources identified: ILOSTAT, INEGI, CONEVAL, IDB project data.",TERRA],
 ["What this cannot tell us","Patents measure registered invention, not all ingenuity, and firms often file abroad instead. R&D years differ by country, 2023 to 2024. Korea's path had a geopolitical sponsor and an authoritarian state. One country is not a counterfactual for another.",SLATE]
].forEach((c,i)=>{
  const x=0.9+i*3.95;
  s.addText(c[0],{ x, y:2.3, w:3.6, h:0.4, fontSize:14, bold:true, color:c[2], isTextBox:true, margin:0 });
  s.addShape(pres.ShapeType.rect,{ x, y:2.76, w:0.5, h:0.025, fill:{color:c[2]} });
  s.addText(c[1],{ x, y:2.95, w:3.6, h:2.5, fontSize:11.5, color:MUTED, isTextBox:true, margin:0 });
});
s.addShape(pres.ShapeType.roundRect,{ x:0.9, y:5.6, w:11.5, h:1.0, fill:{color:WARM}, line:{color:LINE,width:1}, rectRadius:0.05 });
s.addText("Use of generative AI",{ x:1.2, y:5.75, w:4, h:0.3, fontSize:11, bold:true, color:INK, isTextBox:true, margin:0 });
s.addText("We acknowledge the use of Claude (Anthropic) to locate sources, retrieve and recheck the World Bank series with code, and draft and design these slides. The outputs were a basis for slides we revised. The diagnosis and the recommendation are ours.",
  { x:1.2, y:6.05, w:10.9, h:0.5, fontSize:10.5, color:MUTED, isTextBox:true, margin:0 });
s.addText("Frameworks: Prebisch & Singer 1950 · Perroux 1955 · Myrdal 1957 · Hirschman 1958 · Vernon 1966 · Hausmann, Rodrik & Velasco · Levy on informality · course sessions on Core-Periphery, Industrial Location, Economic Complexity, International Cities",{ placeholder:"source" });
s.addNotes("Backup slide. Shown only if asked.");

pres.writeFile({ fileName:"Eight-Patents-LAC-IDB.pptx" }).then(async()=>{
  const { applyTheme } = require("/root/.claude/skills/synced/a6c30f2a-8e02-4996-86a0-22824dcb5dae_8e6b1064-904c-4890-8461-1917a15381bb/pptx/scripts/apply_theme.js");
  await applyTheme("Eight-Patents-LAC-IDB.pptx", THEME);
  console.log("built + themed");
});
