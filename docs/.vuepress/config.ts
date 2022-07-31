import { defineUserConfig } from 'vuepress'
const { defaultTheme } = require('@vuepress/theme-default')
const { searchPlugin } = require('@vuepress/plugin-search')
const { palettePlugin } = require('@vuepress/plugin-palette')

export default defineUserConfig({
    lang: 'zh-CN',
    title: '小扎机器人',
    description: '这是小扎机器人的帮助文档',
    head: [
        ['meta', { name: 'theme-color', content: '#ffffff' }],
        ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ],
    theme: defaultTheme({
        repo: 'xmmmmmovo/ZhaBotV2',
        docsDir: 'docs',
        navbar: [
            { text: '使用说明', link: '/guide/' },
            { text: '部署教程', link: '/deploy/' },
            { text: '更新日志', link: '/changelog.md' },
        ],
        sidebar: {
            '/guide/': [
                {
                    text: '使用说明',
                    collapsable: false,
                    children: [
                        'admin',
                        'bans',
                        'chat',
                        'checkin',
                        'economic',
                        'horserace',
                        'info',
                        'notice_request',
                        'sx',
                        'tasks',
                        'weather',
                        'russian_roulette',
                        'qa'
                    ]
                }
            ]
        }
    }),
    plugins: [
        searchPlugin({}),
        palettePlugin({ preset: 'sass' }),
    ]
})