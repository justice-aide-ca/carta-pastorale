"use client"

import { createContext, useContext, useState, ReactNode } from "react"
import { fr } from "./fr"
import { en } from "./en"

type Lang = "fr" | "en"
type Translations = typeof fr

const translations: Record<Lang, Translations> = { fr, en }

interface I18nContextType {
  lang: Lang
  setLang: (l: Lang) => void
  t: Translations
}

const I18nContext = createContext<I18nContextType>({
  lang: "fr",
  setLang: () => {},
  t: fr,
})

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Lang>("fr")
  return (
    <I18nContext.Provider value={{ lang, setLang, t: translations[lang] }}>
      {children}
    </I18nContext.Provider>
  )
}

export function useI18n() {
  return useContext(I18nContext)
}
