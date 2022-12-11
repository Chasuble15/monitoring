/**
 * Payload Decoder for Chirpstack
 * # Modbus RTU PAC Sanitaire device data
# 0-1 : PAYVER
# 2-5 : Temp haut du ballon
# 6-9 : Temp prise d'air
# 10-13 : Temp collecteur
# 14-17 : Temp consigne
# 18-21 : Temp minimale
# 22-25 : Etat ventilateur
# 26-29 : Etat compresseur
# 30-33 : Etat appoint electrique
# 34-37 : Duree fct appoint electrique
# 38-41 : Puissance active
# 42-45 : Mode de fct
# 46-49 : Temp max en boost
# 50-53 : Duree fct appareil
# 54-57 : Duree fct Ventilateur
# 58-61 : Duree fct Compresseur
# ex: 0100310014001400320019000000000000019500000008003c47f90e010d8f
 * 
 * @product Dragino for Dimplex DHW 300
 */
function decodeUplink(input) {
  
  return {
    data: {
      temp_ballon: (input.bytes[1]<<8)|(input.bytes[2]),
      temp_air: (input.bytes[3]<<8)|(input.bytes[4]),
      temp_collector: (input.bytes[5]<<8)|(input.bytes[6]),
      temp_consigne: (input.bytes[7]<<8)|(input.bytes[8]),
      temp_min: (input.bytes[9]<<8)|(input.bytes[10]),
      state_ventil: (input.bytes[11]<<8)|(input.bytes[12]),
      state_compress: (input.bytes[13]<<8)|(input.bytes[14]),
      state_appoint: (input.bytes[15]<<8)|(input.bytes[16]),
      d_appoint: (input.bytes[17]<<8)|(input.bytes[18]),
      active_power: (input.bytes[19]<<8)|(input.bytes[20]),
      mode: (input.bytes[21]<<8)|(input.bytes[22]),
      temp_max: (input.bytes[23]<<8)|(input.bytes[24]),
      d_appareil: (input.bytes[25]<<8)|(input.bytes[26]),
      d_ventil: (input.bytes[27]<<8)|(input.bytes[28]),
      d_compress: (input.bytes[29]<<8)|(input.bytes[30])
    }
  };
}

function toHexString(byteArray) {
    var s = '0x';
    byteArray.forEach(function(byte) {
      s += ('0' + (byte & 0xFF).toString(16)).slice(-2);
    });
    return s;
}

// Encode downlink function.
//
// Input is an object with the following fields:
// - data = Object representing the payload that must be encoded.
// - variables = Object containing the configured device variables.
//
// Output must be an object with the following fields:
// - bytes = Byte array containing the downlink payload.
function encodeDownlink(input) {
  return {
    bytes: [225, 230, 255, 0]
  };
}