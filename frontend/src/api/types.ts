export type Member={id:number;name:string;photo:string|null;position:string;domain:'HARDWARE'|'SOFTWARE';bio:string;github:string;linkedin:string;email:string};
export type Event={id:number;title:string;description:string;image:string;date:string;location:string;registration_url:string};
export type GalleryImage={id:number;image:string;caption:string;event:number|null};
export type Settings={club_name:string;tagline:string;contact_email:string;instagram_url:string;linkedin_url:string;github_url:string;discord_url:string;college_name:string;footer_text:string};
