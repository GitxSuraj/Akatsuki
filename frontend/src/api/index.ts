import type {Member,Event,GalleryImage,Settings} from './types';
const base=(import.meta.env.VITE_API_URL||'http://127.0.0.1:8000/api').replace(/\/$/,'');
async function get<T>(path:string):Promise<T>{const r=await fetch(`${base}/${path}/`);if(!r.ok)throw new Error('Network');return r.json();}
export const api={members:()=>get<Member[]>('members'),events:()=>get<Event[]>('events'),gallery:()=>get<GalleryImage[]>('gallery'),settings:()=>get<Settings>('settings')};
export async function submitApplication(form:FormData){const r=await fetch(`${base}/applications/`,{method:'POST',body:form});const data=await r.json();if(!r.ok)throw Object.assign(new Error(data.detail||'Submission failed'),{data});return data;}
export function mediaUrl(src:string){if(src.startsWith('http'))return src;const origin=base.replace(/\/api$/,'');return `${origin}${src.startsWith('/')?'':'/'}${src}`;}
