
import { ACTORS } from "../data/actors.js";

const ID = "dorinia-hag-host";
const FLAG = "sourceKey";

Hooks.once("init", () => {
  game.settings.register(ID, "imported", {name:"Doorinia Hag Host imported", scope:"world", config:false, type:Boolean, default:false});
});

Hooks.once("ready", async () => {
  if (!game.user.isGM) return;
  const api = { importAll, rebuild: async () => { await removeImported(); await importAll(true); }, removeImported };
  game.modules.get(ID).api = api;
  if (!game.settings.get(ID, "imported")) await importAll(false);
});

function mod(n){ return Math.floor((n-10)/2); }
function profForCR(cr){ if(cr<5)return 2; if(cr<9)return 3; if(cr<13)return 4; if(cr<17)return 5; if(cr<21)return 6; if(cr<25)return 7; return 8; }
function esc(s){ return String(s??"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
function rollLink(formula,label){ return `[[/r ${formula}]]${label?` ${label}`:""}`; }

function baseActivity(type, name, {activation="action", range=5, target="creature"}={}) {
  const id = foundry.utils.randomID();
  return [id, {
    _id:id, type, name,
    activation:{type:activation,value:1,condition:"",override:false},
    consumption:{scaling:{allowed:false,max:""},spellSlot:false,targets:[]},
    description:{chatFlavor:""},
    duration:{concentration:false,override:false,value:null,units:"inst",special:""},
    effects:[], flags:{},
    range:{override:false,value:range,units:"ft",special:""},
    target:{override:false,prompt:true,template:{count:"",contiguous:false,type:"",size:"",width:"",height:"",units:"ft"},affects:{count:"1",type:target,choice:false,special:""}},
    uses:{spent:0,max:"",recovery:[]}, visibility:{identifier:"",level:{min:null,max:null},requireAttunement:false,requireIdentification:false,requireMagic:false}
  }];
}
function damagePart(formula,type){
  const m=String(formula).replaceAll(" ","").match(/^(\d+)d(\d+)([+-]\d+)?$/i);
  if(m) return {number:Number(m[1]),denomination:Number(m[2]),bonus:m[3]||"",types:[type],custom:{enabled:false,formula:""},scaling:{mode:"",number:null,formula:""}};
  return {number:null,denomination:null,bonus:"",types:[type],custom:{enabled:true,formula:String(formula)},scaling:{mode:"",number:null,formula:""}};
}
function actionItem(a){
  let html=`<p>${esc(a.text)}</p>`;
  let activity;
  if(a.kind==="attack"){
    const r=a.range||a.reach||5;
    html += `<p><strong>Quick rolls:</strong> Attack ${rollLink(`1d20+${a.tohit}`)}; ${a.damage.map(([f,t])=>rollLink(f,t)).join(" + ")}</p>`;
    let [id,b]=baseActivity("attack",a.name,{range:r});
    b.attack={ability:"none",bonus:String(a.tohit),critical:{threshold:20},flat:true,type:{value:a.range?"ranged":"melee",classification:"weapon"}};
    b.damage={critical:{bonus:""},includeBase:true,parts:a.damage.map(([f,t])=>damagePart(f,t))};
    activity={[id]:b};
  } else if(a.kind==="save"){
    html += `<p><strong>Save:</strong> DC ${a.dc} ${a.ability.toUpperCase()}. ${a.damage?.length?`Damage ${a.damage.map(([f,t])=>rollLink(f,t)).join(" + ")}.`:""}</p>`;
    let [id,b]=baseActivity("save",a.name,{range:60});
    b.save={ability:[a.ability],dc:{calculation:"",formula:String(a.dc)}};
    b.damage={onSave:a.onSave||"half",parts:(a.damage||[]).map(([f,t])=>damagePart(f,t))};
    activity={[id]:b};
  } else {
    html += `<p><em>Utility feature; resolve as described.</em></p>`;
    let [id,b]=baseActivity("utility",a.name,{range:60});
    activity={[id]:b};
  }
  return {name:a.name,type:"feat",img:"icons/svg/sword.svg",system:{description:{value:html,chat:""},source:{custom:"Doorinia Hag Host"},activities:activity,uses:{spent:0,max:"",recovery:[]}},flags:{[ID]:{generated:true}}};
}
function textItem(name,text,img="icons/svg/book.svg"){
  return {name,type:"feat",img,system:{description:{value:`<p>${esc(text)}</p>`,chat:""},source:{custom:"Doorinia Hag Host"},activities:{},uses:{spent:0,max:"",recovery:[]}},flags:{[ID]:{generated:true}}};
}
function actorData(m,folderId){
  const p=profForCR(m.cr), abilities={};
  for(const k of ["str","dex","con","int","wis","cha"]) abilities[k]={value:m.abilities[k],proficient:m.saves.includes(k)?1:0};
  const skills={}; for(const [k,v] of Object.entries(m.skills||{})) skills[k]={value:v,ability:"",bonuses:{check:"",passive:""}};
  const items=[
    textItem("Army Role",`${m.role}. ${m.desc||""}`,"icons/svg/target.svg"),
    ...m.traits.map(t=>textItem(t.split('.')[0],t,"icons/svg/aura.svg")),
    ...m.actions.map(actionItem),
    ...m.legendary.map(t=>textItem(`Legendary — ${t.split('.')[0]}`,t,"icons/svg/lightning.svg"))
  ];
  return {
    name:m.name,type:"npc",folder:folderId,img:"icons/svg/mystery-man.svg",
    flags:{[ID]:{generated:true,[FLAG]:m.name}},
    system:{
      abilities,skills,
      attributes:{ac:{calc:"flat",flat:m.ac},hp:{value:m.hp,max:m.hp,temp:0,tempmax:0,formula:String(m.hp)},movement:{walk:m.speed.walk||0,fly:m.speed.fly||0,swim:m.speed.swim||0,climb:m.speed.climb||0,burrow:m.speed.burrow||0,units:"ft",hover:!!m.speed.fly},spellcasting:"cha"},
      details:{cr:m.cr,alignment:"Chaotic Evil",type:{value:m.type,subtype:m.subtype,swarm:"",custom:""},source:{custom:"Doorinia Hag Host"}},
      traits:{size:m.size,languages:{value:m.languages,custom:""},dr:{value:m.res,custom:""},di:{value:m.imm,custom:""},dv:{value:[],custom:""},ci:{value:m.cond,custom:""}}
    },
    prototypeToken:{name:m.name,displayName:20,disposition:-1,bar1:{attribute:"attributes.hp"},texture:{src:"icons/svg/mystery-man.svg"}},
    items
  };
}
async function getOrMakeFolder(name,parent=null){
  let f=game.folders.find(x=>x.type==="Actor"&&x.name===name&&((x.folder?.id??x.folder)===parent));
  if(!f) f=await Folder.create({name,type:"Actor",folder:parent}); return f;
}
async function createGuide(){
  const existing=game.journal.find(j=>j.getFlag(ID,"generated")); if(existing)return;
  const content=`<h1>Doorinia: Yagha Coven War Host</h1>
  <p>The three High Hags began as the terror of Highforest. They now rule conquered regions of Doorinia by draining Archfey power and reorganising their old followers into standing armies.</p>
  <h2>Grandma — Babha Yagha</h2><p><strong>Doctrine:</strong> fear, darkness, soul attrition, layered control. Darklings screen for Hexers and Berbalangs; Soul-Cage Porters anchor the line; Stalkers punish flanks. Grandma fights behind the line and uses minions as conduits and sacrifices.</p>
  <h2>Auntie — Mama Yagha</h2><p><strong>Doctrine:</strong> poison stacking and petrification. Fangguards hold, Coil Adepts restrain, archers exploit poisoned targets, Eye Acolytes force Constitution saves, Chainmasters move warbeasts, and Alchemists deny areas.</p>
  <h2>Gaga — Gahgah Yagha</h2><p><strong>Doctrine:</strong> shock assault. Trolls breach and regenerate, Snail Lancers create an antimagic spearhead, Flail Snails shelter the advance, Spider-Riders pin escape routes, and Rage-Drummers keep the whole host moving.</p>
  <h2>Recommended Combined-Army Wave</h2><p>Start with scouts/skirmishers, then a control layer, then the heavy line, and only then reveal the hag. Mixing factions works best when Grandma supplies control, Auntie supplies poison/petrification, and Gaga supplies forced movement and finishers.</p>
  <h2>Foundry Notes</h2><p>Every damaging action includes clickable inline rolls in its description as a fallback. On D&D5e 5.3.3 the module also creates native Activities for attacks and saves. If another module alters the Activity schema, the inline rolls remain usable.</p>`;
  await JournalEntry.create({name:"Doorinia Hag Host — GM Guide",flags:{[ID]:{generated:true}},pages:[{name:"GM Guide",type:"text",text:{content,format:1}}]});
}
async function importAll(force=false){
  if(!game.user.isGM)return;
  const root=await getOrMakeFolder("Doorinia — Yagha Coven War Host");
  const folders={Grandma:await getOrMakeFolder("Grandma — Babha Yagha",root.id),Auntie:await getOrMakeFolder("Auntie — Mama Yagha",root.id),Gaga:await getOrMakeFolder("Gaga — Gahgah Yagha",root.id)};
  let created=0, failed=[];
  for(const m of ACTORS){
    if(!force && game.actors.find(a=>a.getFlag(ID,FLAG)===m.name)) continue;
    try{ await Actor.create(actorData(m,folders[m.faction]?.id??root.id)); created++; }
    catch(err){
      console.error(`${ID} failed actor ${m.name}`,err); failed.push(m.name);
      // Fallback actor keeps complete text/inline rolls even if an Activity schema was changed by another module.
      try{
        const d=actorData(m,folders[m.faction]?.id??root.id); d.items=d.items.map(i=>({...i,system:{...i.system,activities:{}}}));
        await Actor.create(d); created++; failed=failed.filter(x=>x!==m.name);
      }catch(err2){console.error(`${ID} fallback failed ${m.name}`,err2);}
    }
  }
  await createGuide(); await game.settings.set(ID,"imported",true);
  ui.notifications.info(`Doorinia Hag Host: ${created} actors imported${failed.length?`; ${failed.length} failed — see console`:""}.`);
}
async function removeImported(){
  if(!game.user.isGM)return;
  const actors=game.actors.filter(a=>a.getFlag(ID,"generated")); if(actors.length) await Actor.deleteDocuments(actors.map(a=>a.id));
  const journals=game.journal.filter(j=>j.getFlag(ID,"generated")); if(journals.length) await JournalEntry.deleteDocuments(journals.map(j=>j.id));
  await game.settings.set(ID,"imported",false);
  ui.notifications.info("Doorinia Hag Host generated content removed.");
}
