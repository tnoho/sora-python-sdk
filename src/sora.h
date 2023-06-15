#ifndef SORA_H_
#define SORA_H_

#include <memory>
#include <optional>
#include <vector>

#include "dispose_listener.h"
#include "sora_audio_source.h"
#include "sora_connection.h"
#include "sora_factory.h"
#include "sora_track_interface.h"
#include "sora_video_source.h"

class Sora : public DisposePublisher {
 public:
  Sora(bool use_hardware_encoder);
  ~Sora();

  std::shared_ptr<SoraConnection> CreateConnection(
      const std::string& signaling_url,
      const std::string& role,
      const std::string& channel_id,
      std::optional<std::string> client_id,
      std::optional<std::string> bundle_id,
      const nb::handle& metadata,
      const nb::handle& signaling_notify_metadata,
      SoraTrackInterface* audio_source,
      SoraTrackInterface* video_source,
      std::optional<bool> audio,
      std::optional<bool> video,
      std::optional<std::string> audio_codec_type,
      std::optional<std::string> video_codec_type,
      std::optional<int> video_bit_rate,
      std::optional<int> audio_bit_rate,
      std::optional<bool> simulcast,
      std::optional<bool> spotlight,
      std::optional<int> spotlight_number,
      std::optional<std::string> simulcast_rid,
      std::optional<std::string> spotlight_focus_rid,
      std::optional<std::string> spotlight_unfocus_rid,
      const nb::handle& data_channels,
      std::optional<bool> data_channel_signaling,
      std::optional<bool> ignore_disconnect_websocket,
      std::optional<int> data_channel_signaling_timeout,
      std::optional<int> disconnect_wait_timeout,
      std::optional<int> websocket_close_timeout,
      std::optional<int> websocket_connection_timeout

  );

  SoraAudioSource* CreateAudioSource(size_t channels, int sample_rate);
  SoraVideoSource* CreateVideoSource();

 private:
  boost::json::value ConvertJsonValue(nb::handle value,
                                      const char* error_message);
  std::vector<sora::SoraSignalingConfig::DataChannel> ConvertDataChannels(
      const nb::handle value);

  std::unique_ptr<SoraFactory> factory_;
};
#endif
