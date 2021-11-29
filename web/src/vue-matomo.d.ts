declare module "vue-matomo" {
  import {Vue as _Vue} from "vue/types/vue";
  import VueRouter from "vue-router";

  export const matomoKey: string;

  export interface Options {
    host: string;
    siteId: string;
    router?: VueRouter;
    debug?: boolean;
    disableCookies?: boolean;
    requireCookieConsent?: boolean;
    enableHeartBeatTimer?: boolean;
    enableLinkTracking?: boolean;
    heartBeatTimerInterval?: number;
    requireConsent?: boolean;
    trackInitialView?: boolean;
    trackSiteSearch?: boolean;
    trackerFileName?: string;
    trackerUrl?: string;
    trackerScriptUrl?: string;
    userId?: string;
    cookieDomain?: string;
    domains?: string;
    preInitActions?: any[];
  }

  export default function install(Vue: typeof _Vue, options?: Options): void;
}


