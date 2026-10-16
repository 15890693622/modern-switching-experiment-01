import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL} from 'node:url';
const root=process.cwd(),M=path.join(root,'materials');
const modules=process.env.RUNTIME_NODE_MODULES;if(!modules)throw new Error('Set RUNTIME_NODE_MODULES to the installed @oai/artifact-tool package parent');
const {Presentation,PresentationFile}=await import(pathToFileURL(path.join(modules,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const plan=JSON.parse(await fs.readFile(path.join(M,'slides_plan.json'),'utf8'));const p=Presentation.create({slideSize:{width:1280,height:720}});
function tx(s,name,t,x,y,w,h,size=28,bold=false){const a=s.shapes.add({name,geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});a.text=t;a.text.style={typeface:'SimSun',fontSize:size,bold,color:'#17354A'};return a;}
for(let i=0;i<plan.length;i++){const v=plan[i],s=p.slides.add();s.background.fill='#FAFAF7';tx(s,'title',v.title,64,48,1152,78,40,true);
if(v.image){const f=await fs.readFile(path.join(root,'examples/teacher_results',v.image));s.images.add({blob:f,contentType:'image/png',fit:'contain',position:{left:55,top:165,width:1170,height:440},alt:v.title});tx(s,'caption','教师参考实现结果，参数与假设见实验指导书',64,615,1140,40,24);}
else{v.lines.forEach((t,j)=>tx(s,'reveal-'+j,t,72,175+j*86,1120,76,28));}
tx(s,'footer','现代交换原理 实验01                                      '+(i+1)+' / '+plan.length,64,675,1152,30,20);s.speakerNotes.text=v.note;}
await fs.mkdir(path.join(root,'.build'),{recursive:true});await(await PresentationFile.exportPptx(p)).save(path.join(root,'.build/lecture_slides-draft.pptx'));await fs.copyFile(path.join(root,'.build/lecture_slides-draft.pptx'),path.join(M,'lecture_slides.pptx'));console.log('PPTX generated; office animation refresh is optional');
