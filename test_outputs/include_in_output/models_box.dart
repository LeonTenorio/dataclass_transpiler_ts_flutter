class ModelsBox<T> {
  final Future<void> Function(String key, T value) _put;
  final T? Function(String key) _get;
  final Future<void> Function(String key) _delete;
  final Future<void> Function() _clear;
  final Iterable<T> Function() _values;
  final Iterable<String> Function() _keys;

  const ModelsBox({
    required Future<void> Function(String key, T value) put,
    required final T? Function(String key) get,
    required Future<void> Function(String key) delete,
    required Future<void> Function() clear,
    required final Iterable<T> Function() values,
    required final Iterable<String> Function() keys,
  })  : _put = put,
        _get = get,
        _delete = delete,
        _clear = clear,
        _values = values,
        _keys = keys;

  Iterable<String> get keys => _keys();

  int get length => keys.length;

  bool get isEmpty => keys.isEmpty;

  bool get isNotEmpty => !isEmpty;

  T? get(String key) => _get(key);

  Future<void> put(String key, T data) async {
    if (keys.contains(key)) {
      await _delete(key);
    }
    await _put(key, data);
  }

  Future<void> delete(String key) => _delete(key);

  Iterable<T> get values => _values();

  Future<void> clear() => _clear();
}
