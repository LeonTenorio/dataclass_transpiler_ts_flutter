import 'package:freezed_annotation/freezed_annotation.dart';

class DateTimeConverter implements JsonConverter<DateTime, String> {
  const DateTimeConverter();

  @override
  DateTime fromJson(String json) => _timeZoneDateTimeFromJson(json)!;

  @override
  String toJson(DateTime dateTime) => _timeZoneDateTimeToJson(dateTime)!;
}

class NullableDateTimeConverter implements JsonConverter<DateTime?, String?> {
  const NullableDateTimeConverter();

  @override
  DateTime? fromJson(String? json) => _timeZoneDateTimeFromJson(json);

  @override
  String? toJson(DateTime? dateTime) => _timeZoneDateTimeToJson(dateTime);
}

DateTime? _timeZoneDateTimeFromJson(String? json) {
  if (json == null) return null;

  DateTime parsed = DateTime.parse(json);
  return parsed.toLocal();
}

String? _timeZoneDateTimeToJson(DateTime? dateTime) {
  if (dateTime == null) return null;

  return dateTime.subtract(DateTime.now().timeZoneOffset).toIso8601String();
}
