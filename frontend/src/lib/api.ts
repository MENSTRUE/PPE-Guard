import type {ModelResponse,PredictionResponse,HealthResponse} from './types';
const BASE=(import.meta.env.VITE_API_BASE_URL || '/api/v1').replace(/\/$/,'');
async function parseResponse<T>(response:Response):Promise<T>{
 if(!response.ok){ let errorMessage=`HTTP ${response.status}`;try{const body=await response.json();errorMessage=typeof body.detail==='string'?body.detail:JSON.stringify(body.detail||body)}catch{/* response not JSON */}throw new Error(errorMessage); }
 return response.json() as Promise<T>;
}
export async function getHealth(signal?:AbortSignal){return parseResponse<HealthResponse>(await fetch(`${BASE}/health`,{signal}));}
export async function getModel(signal?:AbortSignal){return parseResponse<ModelResponse>(await fetch(`${BASE}/models`,{signal}));}
export async function predictImage(file:File,confidence:number,signal?:AbortSignal){
 const form=new FormData();form.append('file',file);
 const query=new URLSearchParams({confidence:String(confidence),include_annotated:'true'});
 return parseResponse<PredictionResponse>(await fetch(`${BASE}/predict/image?${query}`,{method:'POST',body:form,signal}));
}
