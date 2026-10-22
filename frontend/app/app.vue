<script setup lang="ts">
import { fr, es, en, pt, pt_br, de, hu, pl, it, ar } from '@nuxt/ui/locale'
import { srCyrl, srLatn } from '~/constants/nuxtUiSerbian'

const { t, locale } = useI18n()

// @nuxt/ui does not ship Tamil or Telugu locales yet; fall back to English for
// built-in UI labels while vue-i18n still serves the app's ta/te messages.
// Serbian is defined locally (constants/nuxtUiSerbian.ts).
const nuxtUILocales: Record<string, typeof en> = { en, fr, es, pt, 'pt-BR': pt_br, de, hu, pl, it, ar, 'ta': en, 'te': en, 'hi': en, 'sr-Cyrl': srCyrl, 'sr-Latn': srLatn }
const nuxtUILocale = computed(() => nuxtUILocales[locale.value] || en)

// Direction comes from the Nuxt UI locale entry (ar has dir: 'rtl').
const htmlDir = computed(() => nuxtUILocale.value.dir ?? 'ltr')

useHead(() => ({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: locale.value,
    dir: htmlDir.value
  }
}))

useSeoMeta({
  title: 'DentalPin',
  description: t('app.tagline')
})
</script>

<template>
  <UApp :locale="nuxtUILocale">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
