# Design references

- Selected PDC00420V SKU EP004131: https://store.easyware.id/produk/pd-trigger-mini-tegangan-tetap/
- Locally listed MP1584 module: https://www.easyware.co.id/product/mp1584-3a-dc-dc-step-down-buck-converter-module-adjustable-33v-5v-9v-12v/
- Alternative local donor/module22x17x4mm: https://cncstorebandung.com/product/mp1584-small-adjustable-step-down-dc-3a-4-5-28v-to-0-8-20v-module/
- MP1584 manufacturer: https://www.monolithicpower.com/en/products/mp1584.html (manufacturer marks it not recommended for new bare-IC designs; selected here as available complete module).
- Buffer TTL-compatible input at5V: https://www.ti.com/product/SN74AHCT1G125
- ESP antenna placement: https://documentation.espressif.com/esp8266_hardware_design_guidelines_en.html
- ESP12F module: https://docs.ai-thinker.com/_media/esp8266/docs/esp-12f_product_specification_en.pdf

Exact AMS1117 donor identity and capacitor ESR requirements still require matching its manufacturer datasheet. Generic1117 families are not automatically interchangeable for stability/thermal purposes.
