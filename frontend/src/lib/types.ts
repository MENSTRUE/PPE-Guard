export type BoundingBox = { x1:number; y1:number; x2:number; y2:number };
export type Detection = { class_id:number; class_name:string; confidence:number; bbox:BoundingBox };
export type PredictionResponse = { model:string; task:string; image:{width:number;height:number;filename:string}; detections:Detection[]; detection_count:number; inference_ms:number; safety_observations:{ppe_detected:string[];source_labeled_absences:string[];compliance_status:string;requires_human_review:boolean;note:string}; annotated_image_base64:string|null };
export type ModelResponse = {model:string;task:string;classes:Record<string,string>;class_count:number;checkpoint_available:boolean;verified_contract?:string;notes?:string[]};
export type HealthResponse = Record<string,unknown>;
